"""Read-only inference and local SHAP evidence for the frozen report model."""
import hashlib
import json
from pathlib import Path
import platform
import sys
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import catboost
from catboost import Pool
import numpy as np
import pandas as pd
from models.CreditRiskModel import CreditRiskModel
from web.analytics import base_model_contributions

OUT = ROOT / 'reports/modeling/selected_model_evaluation_20261030/interpretation/shap_case_study_20261108'
OUT.mkdir(parents=True, exist_ok=True)
model = CreditRiskModel(ROOT).loadModel()
assert model.version == 'catboost-selected-a8763faa0c2ef0786f72'
assert model.family == 'CAT' and len(model.feature_order) == 182
assert model.metadata['use_sigmoid'] is False
assert model.threshold == 0.14539365168823878
ids = [100001, 100005]  # First two rows of the existing unlabelled sample, chosen before SHAP.
source_path = ROOT / 'data/features/b/application_test.parquet'
source = pd.read_parquet(source_path, filters=[('SK_ID_CURR', 'in', ids)]).set_index('SK_ID_CURR').loc[ids]
prepared = model.prepareInput(source.loc[:, model.feature_order])
pool = Pool(prepared, cat_features=model.categorical)
terms = model.model.get_feature_importance(pool, type='ShapValues', thread_count=1)
margin = np.asarray(model.model.predict(pool, prediction_type='RawFormulaVal', thread_count=1))
predicted = model.predict(prepared)
saved = pd.read_csv(OUT.parent / 'sample_predictions.csv').set_index('SK_ID_CURR')
rows, all_terms = [], []
for pos, profile_id in enumerate(ids):
    values = terms[pos, :-1]
    base = float(terms[pos, -1])
    total = float(values.sum())
    score = float(predicted.loc[profile_id, 'score'])
    np.testing.assert_allclose(base + total, margin[pos], rtol=0, atol=1e-10)
    np.testing.assert_allclose(1 / (1 + np.exp(-margin[pos])), score, rtol=0, atol=1e-12)
    np.testing.assert_allclose(score, saved.loc[profile_id, 'score'], rtol=0, atol=1e-12)
    assert bool(predicted.loc[profile_id, 'alert']) == bool(saved.loc[profile_id, 'alert'])
    order = np.argsort(np.abs(values))[::-1]
    shown = base_model_contributions(model, source.loc[[profile_id], model.feature_order])
    assert [x['feature'] for x in shown] == [model.feature_order[j] for j in order[:10]]
    np.testing.assert_allclose([x['value'] for x in shown], values[order[:10]], rtol=0, atol=1e-10)
    top = [{'feature': model.feature_order[j], 'value': float(values[j]),
            'input_value': source.loc[profile_id, model.feature_order[j]]}
           for j in order[:5]]
    # Read input values through pandas JSON to convert numpy scalars and NaN safely.
    inputs = json.loads(source.loc[[profile_id], model.feature_order].to_json(orient='records'))[0]
    for item in top:
        item['input_value'] = inputs[item['feature']]
    rows.append({'SK_ID_CURR': profile_id, 'dataset': 'application_test', 'TARGET_available': False,
                 'score': score, 'threshold': model.threshold,
                 'alert': bool(predicted.loc[profile_id, 'alert']), 'base_value': base,
                 'shap_sum': total, 'raw_margin': float(margin[pos]),
                 'reconstruction_abs_error': float(abs(base + total - margin[pos])),
                 'top5_abs': top, 'remaining_shap_sum': float(values[order[5:]].sum())})
    for j in range(len(values)):
        all_terms.append({'SK_ID_CURR': profile_id, 'feature': model.feature_order[j],
                          'input_value': inputs[model.feature_order[j]], 'shap_value': float(values[j])})

hash_file = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
result = {'date': date.today().isoformat(), 'status': 'passed', 'model_version': model.version,
          'model_sha256': hash_file(ROOT / model.metadata['model_path']),
          'metadata_sha256': hash_file(ROOT / 'artifacts/inference_metadata.json'),
          'source_parquet_sha256': hash_file(source_path),
          'selection_rule': 'First two rows in existing sample_predictions.csv, before computing SHAP; illustrative, not representative',
          'model_refitted': False, 'threshold_changed': False, 'database_modified': False,
          'checks': ['SHAP full sum reconstructs raw margin at atol=1e-10',
                     'sigmoid of raw margin matches predict_proba at atol=1e-12',
                     'scores match frozen sample_predictions.csv at atol=1e-12',
                     'web top 10 features and values match CatBoost SHAP at atol=1e-10'],
          'versions': {'python': platform.python_version(), 'catboost': catboost.__version__,
                       'pandas': pd.__version__, 'numpy': np.__version__}, 'cases': rows}
(OUT / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
pd.DataFrame([{k: v for k, v in row.items() if k != 'top5_abs'} for row in rows]).to_csv(OUT / 'case_summary.csv', index=False)
pd.DataFrame(all_terms).to_csv(OUT / 'shap_values_all_features.csv', index=False)
source.loc[:, model.feature_order].to_parquet(OUT / 'selected_inputs.parquet')
print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))

from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.utils.main_utils import load_object
from sensor.constant.training_pipeline import TARGET_COLUMN
import pandas as pd 
data = pd.read_csv(r"C:\Users\pc\Desktop\_Machine_Learning_Projects\LiveSensor\_testdata.csv")
        #convert it into dataframe 
df = pd.DataFrame(data)
df  = df.drop(columns=['br_000','bq_000','bp_000','ab_000','cr_000','bo_000','bn_000'],axis=1)

model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)

best_model_path = model_resolver.get_best_model_path()
model =load_object(file_path=best_model_path)
y_pred = model.predict(df)
print(y_pred)
df['predicted_column'] = y_pred
df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
print(df.head())

# Import Mage's decorator only if it isn't already loaded
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


# data_exporter: sends data out of the pipeline; df = train_model's 30 predicted rows
@data_exporter
def export_data(df, *args, **kwargs):
    df.to_csv('iris_predictions.csv', index=False)
    print('Saved', len(df), 'predictions to iris_predictions.csv')

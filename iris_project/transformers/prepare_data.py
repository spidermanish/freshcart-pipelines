import pandas as pd
from sklearn.model_selection import train_test_split

# Import Mage's decorators only if they aren't already loaded
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


# transformer: changes data coming from an earlier block (df = load_iris's 150 rows)
@transformer
def transform(df, *args, **kwargs):
    train_df, test_df = train_test_split(df, test_size=0.3, random_state=42)

    train_df = train_df.copy()
    test_df = test_df.copy()
    train_df['split'] = 'train'
    test_df['split'] = 'test'

    result = pd.concat([train_df, test_df])
    print('Train rows:', len(train_df), '| Test rows:', len(test_df))
    return result


# if the 'split' column is missing, this block fails and train_model never runs
@test
def test_output(output, *args):
    assert 'split' in output.columns, 'split column missing'

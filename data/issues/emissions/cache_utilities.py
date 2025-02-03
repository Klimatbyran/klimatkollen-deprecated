import hashlib
import os
import pyarrow.feather as feather

import pandas as pd


def cache_df(f: type(pd.read_excel) = None, path: str = '', freq: str = '1Y') -> type(pd.read_excel):
    """
    Cache the DataFrame to an intermediate file and use it if created within the same period.

    Args:
        f: A function to cache (e.g., a function that loads a DataFrame).
        path: Path to the file to be cached. If provided without f, acts as a decorator.
        freq: Cache period, e.g. '1D', '1M', '1Y'. Defaults to '1Y'. If provided without f, acts as a decorator.

    Returns:
        Caching of the output - not calling the function unless we entered a new period.

    Example usage:

    Create a test Excel file:
        >>> df_test = pd.DataFrame({"A": [1], "B": [2]})
        >>> test_path = "test_data.xlsx"
        >>> df_test.to_excel(test_path, index=False)

    Use the decorator to cache the DataFrame loaded from the file:
        >>> @cache_df
        ... def load_data(path):
        ...     print("Creating DataFrame from file (first call)...")
        ...     return pd.read_excel(path)
        >>> load_data.__name__
        'cache_df_load_data'
        >>> print(load_data(test_path))
        Creating DataFrame from file (first call)...
           A  B
        0  1  2

        >>> print(load_data(test_path))  # Data loaded from cache, no print output
           A  B
        0  1  2

    Use the decorator with a short expiration time:
        >>> @cache_df(path=test_path, freq='1ms')
        ... def load_data_short_expiry(path=test_path):
        ...     print("Creating DataFrame from file (short expiration)...")
        ...     return pd.read_excel(path)
        >>> print(load_data_short_expiry())
        Creating DataFrame from file (short expiration)...
           A  B
        0  1  2

        >>> import time
        >>> time.sleep(0.001)  # Sleep for 1 millisecond

        >>> print(load_data_short_expiry())  # Data expired, loading again from file
        Creating DataFrame from file (short expiration)...
           A  B
        0  1  2

    Clean up the test files:
        >>> file_hash = hashlib.md5(test_path.encode()).hexdigest()
        >>> os.remove(test_path)
        >>> os.remove(f"cache_df_load_data_{file_hash}.feather")
        >>> os.remove(f"cache_df_load_data_{file_hash}.pkl")
        >>> os.remove(f"cache_df_load_data_short_expiry_{file_hash}.feather")
        >>> os.remove(f"cache_df_load_data_short_expiry_{file_hash}.pkl")
    """
    if f is None:
        return lambda f: cache_df(f, path=path, freq=freq)

    def caching_f(*args, **kwargs):
        input_path = kwargs.get('path') or (args[0] if args else path)

        # Create a hash of the path for the cache file
        path_hash = hashlib.md5(input_path.encode()).hexdigest()
        df_file = f'cache_df_{f.__name__}_{path_hash}.feather'
        columns_file = f'cache_df_{f.__name__}_{path_hash}.pkl'

        # Check if cached file and columns file exist and is in the same period as now
        if os.path.exists(df_file):
            stat = os.stat(df_file)
            cache_mtime = pd.Timestamp(stat.st_mtime_ns // 1_000_000, unit='ms')
            if pd.Period(pd.Timestamp.now(), freq=freq) == pd.Period(cache_mtime, freq=freq):
                # Load cached data
                df = pd.read_feather(df_file)
                # Load original column names
                if os.path.exists(columns_file):
                    original_columns = pd.read_pickle(columns_file)
                    df.columns = original_columns
                return df

        # Process and cache the data
        df = f(*args, **kwargs)
        feather.write_feather(df, df_file)

        # Save the original column names separately since feather does not support different heading types
        pd.to_pickle(df.columns, columns_file)

        return df

    caching_f.__name__ = 'cache_df_' + f.__name__
    return caching_f


if __name__ == "__main__":
    import doctest

    doctest.testmod()
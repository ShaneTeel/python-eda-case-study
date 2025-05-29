def clean_transform_extract(csv_file_path, json_file_path, cleaned_csv_file_path):
    '''
    Purpose:
    - Clean: Address errors, duplicates, or NaN/Empty values, if applicable
    - Transform: Convert columns to workable dtype or workable format
    - Extract: Pull relevant data from json df and return it to csv df

    Paramenters:
    - yt_df: the `USvideos.csv` that will serve as the primary df during case study
    - yt_json_df: the `US_category_id.json` that serves as the mechanism for extracting
    category id, name key, value pairs and returning to `yt_df`

    Actions:
    - See comments below 

    Outputs:
    - Cleaned and transformed `yt_df`
    - An array of all unique tags in the `yt_df['tags']` column
    - A dictionary of all `category_id`, `category_name` key, value pairs
    '''
    import pandas as pd
    yt_df = pd.read_csv(csv_file_path)
    yt_json_df = pd.read_json(json_file_path)

    # Converts datetime columns to datetime dtypes based on specific formats
    # Converts `publish_time to UTC datetime format`
    yt_df['publish_time'] = pd.to_datetime(
        arg=yt_df['publish_time'], 
        errors='coerce',
        )
    # Converts `trending_date` to datetime format (`yy-dd-mm`-based)
    yt_df['trending_date'] = pd.to_datetime(
        arg=yt_df['trending_date'], 
        errors='coerce', 
        format='%y.%d.%m',
        )
    
    # Category names
    # Creates a dictionary of category id (keys) and names (values)
    cat_id_name_dict = dict(
        zip(
            yt_json_df['items'].str.get('id').astype(int),
            yt_json_df['items'].str.get('snippet').str.get('title')
            )
        )    
    # Inserts category names into a new column using the dictionary
    # and `category_id` column as a map
    yt_df.insert(
        loc=5, 
        column='category_name', 
        value=yt_df['category_id'].map(cat_id_name_dict)
        )

    # Inserts three new columns based on the `publish_time` column
    # Inserts month column
    yt_df.insert(
        loc=yt_df.columns.get_loc('publish_time') + 1, 
        column='publish_time_month', 
        value=yt_df['publish_time'].dt.month_name()
        )
    # Inserts day of week name column
    yt_df.insert(
        loc=yt_df.columns.get_loc('publish_time') + 2, 
        column='publish_time_day_name', 
        value=yt_df['publish_time'].dt.day_name()
        )
    # Inserts date column
    yt_df.insert(
        loc=yt_df.columns.get_loc('publish_time') + 3, 
        column='publish_time_date', 
        value=yt_df['publish_time'].dt.date
        )

    # Inserts two new columns based on the `trending_date` column
    # Inserts month column
    yt_df.insert(
        loc=yt_df.columns.get_loc('trending_date') + 1, 
        column='trending_date_month', 
        value=yt_df['trending_date'].dt.month_name()
        )
    # Inserts day of week name column
    yt_df.insert(
        loc=yt_df.columns.get_loc('trending_date') + 2, 
        column='trending_date_day_name', 
        value=yt_df['trending_date'].dt.day_name()
        )
    
    range_series = (
    yt_df.groupby('video_id')['trending_date'].max()
      - yt_df.groupby('video_id')['trending_date'].min()
        ).dt.days
    yt_df.insert(
        loc=yt_df.columns.get_loc('trending_date') + 3, 
        column='num_days_trending', 
        value=yt_df['video_id'].map(range_series)
    )

    # Replaces the values in the `tags` column
    # with a list of individual tags as opposed to a single string
    yt_df['tags'] = yt_df['tags'].str.split('|')
    tag_arr = yt_df['tags'].explode().str.strip('"').str.lower().value_counts(ascending=False).drop('[none]')

    yt_df.to_csv(cleaned_csv_file_path, index=False)
   
    # Prints a message containing instructions on what to do next
    print(f"In a separate cell block, execute the following line of code: clean_yt_df = pd.read_csv('{cleaned_csv_file_path}')")
   
    # Returns the tag_dict the dictionary
    return yt_df, tag_arr
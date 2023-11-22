def dataframe_to_html_with_css(df, css_path='/css/default-styles.css'):
    html_data = df.to_html()
    
    html_data_with_css = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
      {html_data}
    </body>
    </html>
    """
    return html_data_with_css

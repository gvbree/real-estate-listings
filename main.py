from etl.web_to_db import execute

if __name__ == "__main__":       
    execute("sale_house", load_type="preview")
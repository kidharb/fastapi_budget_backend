import pandas as pd
import datetime
from io import StringIO
from fastapi import FastAPI, Depends, HTTPException
from fastapi.logger import logger
from pydantic import BaseModel
from sqlalchemy.orm import Session
from pytz import timezone, UTC
import models, database, dependencies, schemas
import uvicorn
import re

app = FastAPI()

def remove_duplicates(text):
    words = text.split()
    return " ".join(sorted(set(words), key=words.index))

class CSVImportRequest(BaseModel):
    csv_text: str

@app.post("/csv_import/")
def csv_import(request: CSVImportRequest, db: Session = Depends(dependencies.get_db)):
#    pdb.set_trace()
    print("csv_import hit")

    csv_text = request.csv_text

    # Sanitize CSV text
    csv_text = re.sub(r'[^\x20-\x7E\n\r,]', '', csv_text).strip()
    csv_data = StringIO(csv_text)

    try:
        df = pd.read_csv(csv_data, delimiter=',', keep_default_na=False)

        expected_headers = ['Nr', 'Account', 'Posting Date', 'Transaction Date', 'Description', 'Original Description', 'Category', 'Money In', 'Money Out', 'Fee', 'Balance']
        if list(df.columns) != expected_headers:
            raise ValueError("Invalid CSV headers")

        # Fill empty fields with 0
        df = df.fillna('')

        # Ensure remove_duplicates is called for string fields
        for col in df.columns:
            if df[col].dtype == object:  # Check if the column type is a string
                df[col] = df[col].apply(remove_duplicates)
            if col in ['Money In', 'Money Out', 'Fee', 'Balance']:
                df[col] = df[col].apply(lambda x: float(x) if x != '' else 0.0)

        df['Transaction Date'] = df['Transaction Date'].apply(lambda x: timezone('UTC').localize(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M')) if isinstance(x, str) else x)

        records_imported = 0
        for _, row in df.iterrows():
            row['Money In'] = float(row['Money In']) if row['Money In'] != '' else 0.0
            row['Money Out'] = float(row['Money Out']) if row['Money Out'] != '' else 0.0
            row['Fee'] = float(row['Fee']) if row['Fee'] != '' else 0.0
            row['Balance'] = float(row['Balance']) if row['Balance'] != '' else 0.0

            existing = db.query(models.Transaction).filter(
                models.Transaction.transaction_date == row['Transaction Date']
            ).first()

            if not existing:
                transaction = models.Transaction(
                    account_number=row['Account'],
                    posting_date=row['Posting Date'],
                    transaction_date=row['Transaction Date'],
                    description=row['Description'],
                    original_description=row['Original Description'],
                    category=row['Category'],
                    money_in=row['Money In'],
                    money_out=row['Money Out'],
                    fees=row['Fee'],
                    balance=row['Balance']
                )
                db.add(transaction)
                records_imported += 1
            else:
                continue

        db.commit()
        return {"message": "CSV data uploaded successfully!", "imported_records": records_imported}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV data: {e}")


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)

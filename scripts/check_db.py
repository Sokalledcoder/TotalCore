import duckdb

def check_counts():
    con = duckdb.connect("tradecore.duckdb", read_only=True)
    
    try:
        ohlcv_count = con.execute("SELECT COUNT(*) FROM market_data").fetchone()[0]
        funding_count = con.execute("SELECT COUNT(*) FROM funding_rates").fetchone()[0]
        oi_count = con.execute("SELECT COUNT(*) FROM open_interest").fetchone()[0]
        
        print(f"OHLCV Rows: {ohlcv_count}")
        print(f"Funding Rate Rows: {funding_count}")
        print(f"Open Interest Rows: {oi_count}")
        
        # Show sample
        if funding_count > 0:
            print("\nSample Funding:")
            print(con.execute("SELECT * FROM funding_rates LIMIT 5").df())
            
        if oi_count > 0:
            print("\nSample OI:")
            print(con.execute("SELECT * FROM open_interest LIMIT 5").df())
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    check_counts()

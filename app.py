# แก้ไขส่วนนี้ใน app.py
@st.cache_data(ttl=60) # ตั้งให้ดึงข้อมูลใหม่ทุก 60 วินาที
def load_data():
    # ---------------------------------------------------------
    # เอา Link CSV ที่ได้จากการ Publish to web มาวางแทนที่ตรงนี้
    gsheet_url = "https://docs.google.com/spreadsheets/d/e/...../pub?output=csv" 
    # ---------------------------------------------------------
    
    try:
        df = pd.read_csv(gsheet_url)
        
        # Clean data: แปลง DayLeft เป็นตัวเลข
        # (ต้องจัดการกรณีข้อมูลอาจจะเป็น string หรือมี comma)
        if 'DayLeft' in df.columns:
            df['DayLeft'] = df['DayLeft'].astype(str).str.replace(',', '').str.replace('"', '')
            df['DayLeft'] = pd.to_numeric(df['DayLeft'], errors='coerce').fillna(0).astype(int)
        
        # Clean data: เติมค่าว่าง
        df = df.fillna("ไม่ระบุ")
        
        # สร้างฟังก์ชันเช็คสถานะ
        def get_status(day_left):
            if day_left < 0:
                return "Expired (หมดอายุ)"
            elif day_left <= 90:
                return "Expiring Soon (ใกล้หมด)"
            else:
                return "OK (ปกติ)"
        
        if 'DayLeft' in df.columns:
            df['Status'] = df['DayLeft'].apply(get_status)
        else:
            df['Status'] = "ไม่ระบุ"
            
        return df
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการดึงข้อมูล: {e}")
        return pd.DataFrame()

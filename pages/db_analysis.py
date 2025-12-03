# pages/db_analysis.py - Chinook DB 분석 페이지

import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# 데이터 경로 설정 (현재 파일 기준 상대 경로)
# pages/db_analysis.py → ../data/chinook.db
DB_PATH = Path(__file__).parent.parent / "data" / "chinook.db"


@st.cache_resource
def get_connection():
    """DB 연결"""
    return sqlite3.connect(DB_PATH, check_same_thread=False)


@st.cache_data
def load_data(query):
    """쿼리 실행 및 데이터 로드"""
    conn = get_connection()
    return pd.read_sql(query, conn)


# 페이지 설정
st.title("🎵 Chinook 음악 DB 분석")
st.markdown("음악 스트리밍 서비스 데이터를 분석합니다.")

# DB 연결 확인
try:
    conn = get_connection()
    st.success(f"✅ DB 연결 성공: `{DB_PATH.name}`")
except Exception as e:
    st.error(f"❌ DB 연결 실패: {e}")
    st.stop()

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📊 기본 통계", "🎤 아티스트 분석", "💰 매출 분석"])

with tab1:
    st.subheader("데이터베이스 개요")

    # 테이블별 레코드 수
    tables_query = """
        SELECT 'artists' as 테이블, COUNT(*) as 레코드수 FROM artists
        UNION ALL SELECT 'albums', COUNT(*) FROM albums
        UNION ALL SELECT 'tracks', COUNT(*) FROM tracks
        UNION ALL SELECT 'genres', COUNT(*) FROM genres
        UNION ALL SELECT 'customers', COUNT(*) FROM customers
        UNION ALL SELECT 'invoices', COUNT(*) FROM invoices
    """
    df_tables = load_data(tables_query)

    col1, col2, col3 = st.columns(3)
    col1.metric("🎤 아티스트", f"{df_tables[df_tables['테이블']=='artists']['레코드수'].values[0]:,}")
    col2.metric("💿 앨범", f"{df_tables[df_tables['테이블']=='albums']['레코드수'].values[0]:,}")
    col3.metric("🎵 트랙", f"{df_tables[df_tables['테이블']=='tracks']['레코드수'].values[0]:,}")

    st.dataframe(df_tables, width="stretch", hide_index=True)

with tab2:
    st.subheader("인기 아티스트 TOP 10")

    artist_query = """
        SELECT ar.Name as 아티스트, COUNT(t.TrackId) as 트랙수
        FROM artists ar
        JOIN albums al ON ar.ArtistId = al.ArtistId
        JOIN tracks t ON al.AlbumId = t.AlbumId
        GROUP BY ar.ArtistId
        ORDER BY 트랙수 DESC
        LIMIT 10
    """
    df_artists = load_data(artist_query)
    st.bar_chart(df_artists.set_index("아티스트"))

    st.subheader("장르별 트랙 분포")
    genre_query = """
        SELECT g.Name as 장르, COUNT(t.TrackId) as 트랙수
        FROM genres g
        JOIN tracks t ON g.GenreId = t.GenreId
        GROUP BY g.GenreId
        ORDER BY 트랙수 DESC
    """
    df_genres = load_data(genre_query)
    st.bar_chart(df_genres.set_index("장르"))

with tab3:
    st.subheader("국가별 매출")

    sales_query = """
        SELECT c.Country as 국가,
               ROUND(SUM(i.Total), 2) as 총매출,
               COUNT(DISTINCT c.CustomerId) as 고객수
        FROM customers c
        JOIN invoices i ON c.CustomerId = i.CustomerId
        GROUP BY c.Country
        ORDER BY 총매출 DESC
        LIMIT 10
    """
    df_sales = load_data(sales_query)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**💵 매출 순위**")
        st.dataframe(df_sales, width="stretch", hide_index=True)

    with col2:
        st.markdown("**📈 매출 차트**")
        st.bar_chart(df_sales.set_index("국가")["총매출"])

    # 월별 매출 트렌드
    st.subheader("월별 매출 트렌드")
    monthly_query = """
        SELECT strftime('%Y-%m', InvoiceDate) as 월,
               ROUND(SUM(Total), 2) as 매출
        FROM invoices
        GROUP BY 월
        ORDER BY 월
    """
    df_monthly = load_data(monthly_query)
    st.line_chart(df_monthly.set_index("월"))

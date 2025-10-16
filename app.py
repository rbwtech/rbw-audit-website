import streamlit as st
from config import API_KEY, EDUCATION_SITES, ECOMMERCE_SITES, DANGEROUS_SITES
from safe_browsing import SafeBrowsingChecker

# Page config
st.set_page_config(
    page_title="Safe Browsing Checker",
    page_icon="🔒",
    layout="wide"
)

# Initialize checker
@st.cache_resource
def get_checker():
    return SafeBrowsingChecker(API_KEY)

checker = get_checker()

# Title
st.title("🔒 Safe Browsing Checker")
st.markdown("Cek keamanan website menggunakan Google Safe Browsing API")
st.divider()

# Tabs
tab1, tab2 = st.tabs(["📋 Scan Kategori", "🔗 Input URL Manual"])

# Tab 1: Category Scan
with tab1:
    st.subheader("Pilih Kategori Website")
    
    category = st.selectbox(
        "Kategori:",
        ["Website Pendidikan", "Website E-Commerce", "Website Berbahaya"]
    )
    
    if st.button("🔍 Scan Kategori", key="scan_category", use_container_width=True):
        # Determine URLs based on category
        if category == "Website Pendidikan":
            urls = EDUCATION_SITES
            cat_name = "Pendidikan"
        elif category == "Website E-Commerce":
            urls = ECOMMERCE_SITES
            cat_name = "E-Commerce"
        else:
            urls = DANGEROUS_SITES
            cat_name = "Berbahaya"
        
        st.info(f"Memulai scanning kategori: **{cat_name}**")
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Results container
        results_container = st.container()
        
        # Check URLs
        results = []
        total = len(urls)
        
        for idx, url in enumerate(urls):
            status_text.text(f"Scanning {idx + 1}/{total}: {url}")
            is_safe, threats = checker.check_url(url)
            results.append((url, is_safe, threats))
            progress_bar.progress((idx + 1) / total)
        
        status_text.empty()
        progress_bar.empty()
        
        # Display results
        with results_container:
            st.success("✅ Scan selesai!")
            st.divider()
            
            safe_count = sum(1 for _, is_safe, _ in results if is_safe)
            unsafe_count = sum(1 for _, is_safe, _ in results if is_safe == False)
            error_count = sum(1 for _, is_safe, _ in results if is_safe is None)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Aman", safe_count, delta=None)
            col2.metric("Berbahaya", unsafe_count, delta=None)
            col3.metric("Error", error_count, delta=None)
            
            st.divider()
            
            for url, is_safe, threats in results:
                if is_safe is None:
                    with st.expander(f"⚠️ {url} - Error"):
                        st.error(f"**Status:** Error")
                        st.write(f"**Detail:** {threats[0]}")
                elif is_safe:
                    with st.expander(f"✅ {url} - Aman"):
                        st.success("**Status:** Website aman untuk diakses")
                else:
                    with st.expander(f"❌ {url} - Terdeteksi Ancaman", expanded=True):
                        st.error("**Status:** Terdeteksi ancaman!")
                        st.write(f"**Jenis Ancaman:** {', '.join(threats)}")

# Tab 2: Manual URL
with tab2:
    st.subheader("Input URL Manual")
    
    url_input = st.text_input(
        "Masukkan URL:",
        placeholder="https://example.com",
        help="URL akan otomatis ditambahkan https:// jika tidak ada protokol"
    )
    
    if st.button("🔍 Scan URL", key="scan_manual", use_container_width=True):
        if not url_input.strip():
            st.error("⚠️ URL tidak boleh kosong!")
        else:
            url = url_input.strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            st.info(f"Memulai scanning: **{url}**")
            
            with st.spinner("Scanning..."):
                is_safe, threats = checker.check_url(url)
            
            st.divider()
            
            if is_safe is None:
                st.error("❌ **Error**")
                st.write(f"**Detail:** {threats[0]}")
            elif is_safe:
                st.success("✅ **Website Aman**")
                st.write("Website ini aman untuk diakses berdasarkan Google Safe Browsing API")
            else:
                st.error("❌ **Terdeteksi Ancaman!**")
                st.write(f"**Jenis Ancaman:** {', '.join(threats)}")
                st.warning("⚠️ Tidak disarankan untuk mengakses website ini")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    <p>Powered by Google Safe Browsing API | Made with ❤️ by RBW Tech</p>
</div>
""", unsafe_allow_html=True)
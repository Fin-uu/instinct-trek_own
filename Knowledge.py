import streamlit as st

st.set_page_config(page_title="知識庫管理", page_icon="🗂️", layout="wide")

st.title("🗂️ 知識庫管理")

# 上傳文件
st.subheader("📤 上傳知識文件")
uploaded_file = st.file_uploader("支援格式: TXT, PDF, DOCX", type=['txt', 'pdf', 'docx'])

if uploaded_file:
    st.success(f"✅ 已上傳: {uploaded_file.name}")
    if st.button("🔄 向量化並加入知識庫"):
        with st.spinner("處理中..."):
            st.success("✅ 已成功加入知識庫！")

st.divider()

# 知識庫列表
st.subheader("📚 現有知識庫")
knowledge_items = [
    {"標題": "退貨政策", "更新時間": "2024-03-15", "狀態": "✅ 啟用"},
    {"標題": "運送時間", "更新時間": "2024-03-14", "狀態": "✅ 啟用"},
    {"標題": "付款方式", "更新時間": "2024-03-13", "狀態": "✅ 啟用"},
    {"標題": "會員優惠", "更新時間": "2024-03-12", "狀態": "✅ 啟用"},
]

for item in knowledge_items:
    with st.expander(f"📄 {item['標題']} - {item['更新時間']}"):
        st.write(f"**狀態**: {item['狀態']}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("✏️ 編輯", key=f"edit_{item['標題']}")
        with col2:
            st.button("🔄 重新向量化", key=f"vector_{item['標題']}")
        with col3:
            st.button("🗑️ 刪除", key=f"delete_{item['標題']}")
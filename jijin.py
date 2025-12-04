import streamlit as st
import numpy as np

# --- 1. 쓰나미 발생 확률 계산 모델 (예시) ---
# 실제 모델이 아닌, 교육용/데모용으로 단순화된 함수입니다.
def calculate_tsunami_probability(magnitude, depth, latitude, longitude, distance_to_coast):
    """
    지진 매개변수를 기반으로 쓰나미 발생 '위험 지수'를 계산합니다.
    (0~100 사이의 임의의 점수로, 확률이라고 가정합니다.)
    """
    
    # a. 지진 규모(Magnitude)의 영향: 규모가 클수록 위험 증가
    # (예: 규모 6.5 미만은 낮은 영향, 8.0 이상은 매우 높은 영향)
    mag_weight = max(0, (magnitude - 6.5) * 20)
    
    # b. 깊이(Depth)의 영향: 얕을수록(해저면 근처) 위험 증가
    # (예: 50km 미만은 위험, 20km 미만은 더 위험)
    depth_weight = 0
    if depth <= 50:
        depth_weight = 50 - depth
    
    # c. 해안까지의 거리(Distance to Coast)의 영향: 가까울수록 위험 증가
    # (예: 50km 미만은 위험, 10km 미만은 매우 위험)
    dist_weight = max(0, 50 - distance_to_coast) * 0.5
    
    # d. 위도/경도(Latitude/Longitude)의 영향 (예시로 특정 위험 지역 가중치 부여)
    # 실제로는 해당 지역의 쓰나미 발생 기록 및 해저 지형에 따라 복잡하게 결정됩니다.
    # 여기서는 단순화를 위해 가중치를 0으로 설정하거나, 특정 범위에서만 추가 가중치를 부여할 수 있습니다.
    location_weight = 0
    
    # 총 위험 지수 계산 (최대 100을 넘지 않도록 조정)
    risk_index = mag_weight + depth_weight + dist_weight + location_weight
    
    # 최종적으로 0~100 사이의 값으로 정규화 (최대 위험 지수를 150으로 가정)
    probability = min(100, (risk_index / 150) * 100)
    
    return probability

# --- 2. 쓰나미 경보 및 대피 요령 ---

def display_tsunami_info(probability):
    st.subheader("🚨 쓰나미 경보 및 권고사항")
    
    if probability >= 70:
        # 위험 레벨 1: 매우 높음
        st.error("### 🔴 **즉시 대피하세요! 쓰나미 발생 확률이 매우 높습니다.**")
        st.markdown(f"**예측 위험 지수: {probability:.2f}%**")
        st.warning("**최대 위험!** 지진 발생 후 수분 내에 대규모 쓰나미가 도달할 수 있습니다. **가장 높은 곳으로 즉시 이동하세요.**")
        
    elif probability >= 40:
        # 위험 레벨 2: 높음
        st.warning("### 🟠 **쓰나미 발생 가능성 높음! 경계 태세를 갖추고 대피를 준비하세요.**")
        st.markdown(f"**예측 위험 지수: {probability:.2f}%**")
        st.info("해안가 저지대 주민은 즉시 고지대로 이동할 준비를 하십시오. 라디오나 TV로 공식 경보를 주시하세요.")

    elif probability >= 10:
        # 위험 레벨 3: 보통
        st.info("### 🟡 **주의! 쓰나미 발생 가능성이 있습니다. 상황을 주시하세요.**")
        st.markdown(f"**예측 위험 지수: {probability:.2f}%**")
        st.caption("해안가에 있다면 바다의 이상 징후(갑작스러운 해수면 후퇴 등)를 관찰하고, 대피 계획을 확인하세요.")

    else:
        # 위험 레벨 4: 낮음
        st.success("### 🟢 **현재 쓰나미 발생 위험이 낮습니다.**")
        st.markdown(f"**예측 위험 지수: {probability:.2f}%**")
        st.caption("하지만 강한 지진을 느꼈다면 언제든지 경계심을 늦추지 마십시오. 안전한 곳에 머무르세요.")

    st.markdown("---")
    
    # 공통 대피 요령
    st.subheader("📢 **쓰나미 대피 일반 요령**")
    st.markdown("""
    * **즉시 대피:** 지진으로 인해 땅이 심하게 흔들리면 쓰나미 경보 없이도 즉시 고지대로 대피하십시오.
    * **고지대 이동:** 해안에서 멀리 떨어진 **가장 높은 지점**으로 신속하게 이동해야 합니다.
    * **운전 금지:** 차량 대신 **걸어서** 대피하는 것이 더 빠르고 안전할 수 있습니다. 대피로의 정체를 유발하지 마세요.
    * **경보 해제 확인:** 공식적인 **쓰나미 경보 해제 발표**가 있기 전까지는 절대 해안가로 돌아오지 마세요. 쓰나미는 한 번의 파도로 끝나지 않습니다.
    * **정보 수신:** 라디오, TV, 재난 문자 등을 통해 **공식적인 정보**를 지속적으로 확인하세요.
    """)
    


# --- 3. Streamlit 앱 레이아웃 설정 ---

st.set_page_config(page_title="쓰나미 위험 예측 및 경보 시스템", layout="wide")

st.title("🌏 쓰나미 위험 예측 시뮬레이터")
st.markdown("---")

st.header("1. 지진 매개변수 입력")

# 사용자 입력 섹션 (Streamlit 위젯)
with st.sidebar:
    st.header("지진 정보 입력")
    magnitude = st.slider("지진 규모 (Magnitude)", 4.0, 9.5, 7.5, 0.1, help="리히터 규모 또는 모멘트 규모")
    depth = st.slider("지진 깊이 (Depth in km)", 0, 500, 20, 1, help="지표면 아래 발생 깊이 (얕을수록 위험)")
    
    # 위도 및 경도 (예시)
    latitude = st.number_input("위도 (Latitude)", -90.0, 90.0, 38.0, 0.01)
    longitude = st.number_input("경도 (Longitude)", -180.0, 180.0, 129.0, 0.01)
    
    distance_to_coast = st.slider("해안까지의 거리 (Distance to Coast in km)", 0, 500, 50, 5, help="진앙지(epicenter)에서 가장 가까운 해안선까지의 수평 거리")

st.markdown("""
    **⚠️ 시뮬레이션 목적의 단순화된 모델입니다.**
    정확한 예측을 위해서는 전문적인 지진 해일 모델링이 필요합니다.
""")

st.markdown("---")
st.header("2. 예측 결과")

# 버튼 클릭 시 예측 실행
if st.button("쓰나미 위험 예측 실행", type="primary"):
    
    # 모델 실행
    probability = calculate_tsunami_probability(
        magnitude, depth, latitude, longitude, distance_to_coast
    )
    
    # 결과 출력
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("입력된 지진 데이터")
        st.table({
            "변수": ["규모", "깊이", "위도", "경도", "해안 거리"],
            "값": [
                f"{magnitude} M", 
                f"{depth} km", 
                f"{latitude}°", 
                f"{longitude}°", 
                f"{distance_to_coast} km"
            ]
        })

    with col2:
        st.subheader("예측 위험 지수")
        # 게이지 또는 지표 표시
        st.metric(label="쓰나미 발생 위험 지수", value=f"{probability:.2f}%", delta_color="off")
        
        # 위험도에 따른 시각적 피드백
        if probability >= 70:
            st.error("매우 높음")
        elif probability >= 40:
            st.warning("높음")
        elif probability >= 10:
            st.info("보통")
        else:
            st.success("낮음")
            
    st.markdown("---")
    
    # 경보 및 대피 요령 표시
    display_tsunami_info(probability)
else:
    st.info("왼쪽 사이드바에서 지진 정보를 입력하고 '쓰나미 위험 예측 실행' 버튼을 눌러주세요.")

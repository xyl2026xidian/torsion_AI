import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import time

st.set_page_config(page_title="圆轴扭转 · 智能学习系统", layout="wide")

# ========== 侧边栏 ==========
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/gear.png", width=80)
    st.title("🔄 圆轴扭转")
    st.markdown("**智能学习系统**")
    st.markdown("---")

    module = st.radio(
        "选择模块",
        ["📖 理论体系",
         "📊 应力应变计算",
         "💪 强度与刚度设计",
         "🏗️ 工程应用",
         "📐 案例分析",
         "🎨 应力云图",
         "🔄 3D变形动画",
         "🧪 虚拟实验"]
    )
    st.markdown("---")
    st.caption("💡 交互式学习 | 实时可视化 | 工程实战")

# ========== 初始化 ==========
if "tor_data" not in st.session_state:
    st.session_state.tor_data = {
        "T": 2000, "d": 50, "L": 1.0, "G": 80, "material": "40Cr钢"
    }

# 材料数据库
MATERIALS = {
    "Q235钢": {"G": 79, "tau_s": 120, "tau_b": 180, "rho": 7850},
    "45钢": {"G": 80, "tau_s": 150, "tau_b": 220, "rho": 7850},
    "40Cr钢": {"G": 80, "tau_s": 180, "tau_b": 260, "rho": 7850},
    "铝合金": {"G": 26, "tau_s": 160, "tau_b": 200, "rho": 2700},
    "铜合金": {"G": 40, "tau_s": 80, "tau_b": 120, "rho": 8900},
    "钛合金": {"G": 42, "tau_s": 350, "tau_b": 450, "rho": 4430},
}


def set_chinese_font(fig):
    fig.update_layout(
        font=dict(family="SimHei, Microsoft YaHei, Arial Unicode MS, sans-serif")
    )
    return fig


# ============================================================
# 1. 理论体系
# ============================================================
if module == "📖 理论体系":
    st.title("📖 圆轴扭转 · 理论体系")

    tab1, tab2, tab3, tab4 = st.tabs(["📌 基本概念", "📐 核心公式", "📊 材料性能", "🔗 知识图谱"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 📌 什么是圆轴扭转？

            当杆件两端受到**大小相等、方向相反**的力偶作用时，
            杆件产生**扭转变形**。

            **工程实例**：
            - 汽车传动轴
            - 机床主轴
            - 电动机转轴
            - 钻头（螺旋槽）
            - 舵机的输出轴

            ### 📌 变形特点
            - 横截面**绕轴线**发生相对转动
            - 各横截面仍保持**平面**（平截面假设）
            - 轴向纤维不发生伸缩（无正应力）
            - 横截面上只产生**切应力**
            """)
        with col2:
            st.markdown("""
            ### 📌 受力特点
            - 外力为**力偶矩**（扭矩）
            - 扭矩矢量沿**轴线方向**
            - 横截面上无正应力
            - 切应力沿**半径线性分布**

            ### 📌 基本假设
            1. **平截面假设**：变形后截面仍为平面
            2. **线弹性假设**：τ ≤ τ_p
            3. **小变形假设**：扭转角很小
            4. **各向同性假设**：各方向性能相同
            """)

    with tab2:
        st.markdown("""
        ### 📐 核心公式

        #### 1. 切应力公式
        $$\\tau_\\rho = \\frac{T \\cdot \\rho}{J_p}$$
        - $\\tau_\\rho$ — 距圆心 $\\rho$ 处的切应力 (Pa)
        - $T$ — 截面上的扭矩 (N·m)
        - $\\rho$ — 到圆心的距离 (m)
        - $J_p$ — 极惯性矩 (m⁴)

        #### 2. 极惯性矩
        **实心圆轴**：
        $$J_p = \\frac{\\pi d^4}{32}$$

        **空心圆轴**（内径 $d_1$，外径 $d_2$）：
        $$J_p = \\frac{\\pi(d_2^4 - d_1^4)}{32}$$

        #### 3. 最大切应力（在轴表面）
        $$\\tau_{\\max} = \\frac{T \\cdot R}{J_p} = \\frac{16T}{\\pi d^3}$$

        #### 4. 扭转角公式
        $$\\varphi = \\frac{T \\cdot L}{G \\cdot J_p}$$
        - $\\varphi$ — 扭转角 (rad)
        - $L$ — 轴长 (m)
        - $G$ — 剪切模量 (Pa)

        #### 5. 单位长度扭转角
        $$\\theta = \\frac{\\varphi}{L} = \\frac{T}{G \\cdot J_p}$$

        #### 6. 强度条件
        $$\\tau_{\\max} \\leq [\\tau] = \\frac{\\tau_s}{n}$$

        #### 7. 刚度条件
        $$\\theta_{\\max} \\leq [\\theta]$$
        """)

    with tab3:
        st.markdown("""
        ### 📊 常用材料的扭转性能

        | 材料 | 剪切模量 G (GPa) | 剪切屈服强度 τ_s (MPa) | 剪切强度 τ_b (MPa) |
        |------|------------------|------------------------|-------------------|
        | Q235钢 | 79 | 120 | 180 |
        | 45钢 | 80 | 150 | 220 |
        | 40Cr钢 | 80 | 180 | 260 |
        | 铝合金 | 26 | 160 | 200 |
        | 铜合金 | 40 | 80 | 120 |
        | 钛合金 | 42 | 350 | 450 |

        ### 📌 关系式
        $$G = \\frac{E}{2(1+\\nu)}$$
        其中 $\\nu$ 为泊松比
        """)

    with tab4:
        st.markdown("### 🧠 知识图谱")
        st.graphviz_chart('''
        digraph {
            "圆轴扭转" -> "基本概念"
            "圆轴扭转" -> "应力分析"
            "圆轴扭转" -> "变形分析"
            "圆轴扭转" -> "强度设计"
            "圆轴扭转" -> "刚度设计"
            "基本概念" -> "扭矩"
            "基本概念" -> "极惯性矩"
            "应力分析" -> "切应力公式"
            "应力分析" -> "最大切应力"
            "变形分析" -> "扭转角"
            "变形分析" -> "单位扭转角"
            "强度设计" -> "强度条件"
            "刚度设计" -> "刚度条件"
            "切应力公式" -> "τ=Tρ/J"
            "最大切应力" -> "τ=16T/(πd³)"
            "扭转角" -> "φ=TL/(GJ)"
        }
        ''')


# ============================================================
# 2. 应力应变计算
# ============================================================
elif module == "📊 应力应变计算":
    st.title("📊 应力应变计算器")
    st.markdown("输入参数，实时计算扭转应力和变形")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown("### ⚙️ 输入参数")

        T = st.slider("扭矩 T (N·m)", 0, 10000, 2000, 100)
        L = st.slider("轴长 L (m)", 0.1, 3.0, 1.0, 0.1)

        section_type = st.selectbox("截面类型", ["实心圆轴", "空心圆轴"])
        if section_type == "实心圆轴":
            d = st.slider("直径 d (mm)", 10, 200, 50, 2)
            J = np.pi * (d / 1000) ** 4 / 32
            d_inner = 0
        else:
            D = st.slider("外径 D (mm)", 20, 250, 60, 2)
            d_inner = st.slider("内径 d₁ (mm)", 5, D - 5, 30, 2)
            J = np.pi * ((D / 1000) ** 4 - (d_inner / 1000) ** 4) / 32
            d = D

        material = st.selectbox("材料", list(MATERIALS.keys()))
        mat = MATERIALS[material]
        G = mat["G"] * 1e9

        st.session_state.tor_data["T"] = T
        st.session_state.tor_data["d"] = d
        st.session_state.tor_data["L"] = L
        st.session_state.tor_data["G"] = G
        st.session_state.tor_data["material"] = material

        # 计算
        R = d / 2000
        tau_max = T * R / J
        phi = T * L / (G * J)
        theta = phi / L
        tau_s = mat["tau_s"] * 1e6
        n = 2.0
        tau_allow = tau_s / n

        st.markdown("---")
        st.markdown("### 📊 计算结果")

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("最大切应力 τ_max", f"{tau_max / 1e6:.2f} MPa")
            st.metric("扭转角 φ", f"{phi * 180 / np.pi:.4f}°")
        with col_b:
            st.metric("单位扭转角 θ", f"{theta * 180 / np.pi:.4f}°/m")
            st.metric("许用应力 [τ]", f"{tau_allow / 1e6:.1f} MPa")

        if tau_max <= tau_allow:
            st.success(f"✅ 强度满足: {tau_max / 1e6:.1f} ≤ {tau_allow / 1e6:.1f} MPa")
        else:
            st.error(f"❌ 强度不满足: {tau_max / 1e6:.1f} > {tau_allow / 1e6:.1f} MPa")

    with col2:
        # 切应力分布图
        r = np.linspace(0, d / 2, 50)
        tau = tau_max * (r / (d / 2)) / 1e6

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=r, y=tau, mode='lines+markers',
                                 name='切应力分布', fill='tozeroy',
                                 line=dict(color='orange', width=4)))
        fig.add_annotation(x=d / 4, y=max(tau) / 2, text="τ ∝ ρ", showarrow=False, font_size=16)
        fig.update_layout(
            title="切应力沿半径分布 (线性)",
            xaxis_title="半径 ρ (mm)",
            yaxis_title="切应力 τ (MPa)",
            height=350
        )
        fig = set_chinese_font(fig)
        st.plotly_chart(fig, use_container_width=True)

        # 应力-应变关系
        st.markdown("#### 📈 剪切应力-应变曲线")
        gamma = np.linspace(0, 0.01, 50)
        tau_curve = G * gamma / 1e6
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=gamma * 1000, y=tau_curve, mode='lines',
                                  name='τ-γ曲线', line=dict(color='green', width=3)))
        fig2.add_trace(go.Scatter(x=[tau_max / G * 1000], y=[tau_max / 1e6], mode='markers',
                                  marker=dict(color='red', size=16, symbol='star'),
                                  name='当前状态'))
        fig2.update_layout(title="剪切应力-应变曲线 (τ = Gγ)",
                           xaxis_title="切应变 γ (×10⁻³)",
                           yaxis_title="切应力 τ (MPa)",
                           height=250)
        fig2 = set_chinese_font(fig2)
        st.plotly_chart(fig2, use_container_width=True)


# ============================================================
# 3. 强度与刚度设计
# ============================================================
elif module == "💪 强度与刚度设计":
    st.title("💪 强度与刚度设计")
    st.markdown("基于强度和刚度条件进行轴的设计与校核")

    design_mode = st.radio("设计模式", ["强度校核", "直径设计", "许用扭矩计算"], horizontal=True)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("### ⚙️ 设计参数")

        if design_mode == "强度校核":
            T = st.number_input("扭矩 T (N·m)", value=2000, step=100, min_value=10)
            d = st.slider("轴直径 d (mm)", 10, 150, 50, 2)
            material = st.selectbox("材料", list(MATERIALS.keys()))
            mat = MATERIALS[material]
            n = st.slider("安全系数 n", 1.5, 4.0, 2.0, 0.5)
            tau_allow = mat["tau_s"] / n

            J = np.pi * (d / 1000) ** 4 / 32
            tau_max = T * (d / 2000) / J / 1e6

            st.markdown("---")
            st.markdown("### 📋 校核结果")
            st.metric("实际应力", f"{tau_max:.2f} MPa")
            st.metric("许用应力", f"{tau_allow:.2f} MPa")

            if tau_max <= tau_allow:
                st.success(f"✅ 强度通过！安全裕度 {(tau_allow / tau_max - 1) * 100:.1f}%")
            else:
                st.error(f"❌ 强度不通过！应力超 {tau_max / tau_allow - 1:.1f}%")

        elif design_mode == "直径设计":
            T = st.number_input("扭矩 T (N·m)", value=2000, step=100, min_value=10)
            material = st.selectbox("材料", list(MATERIALS.keys()))
            mat = MATERIALS[material]
            n = st.slider("安全系数 n", 1.5, 4.0, 2.0, 0.5)
            tau_allow = mat["tau_s"] / n

            # 由 τ = 16T/(πd³) 反推直径
            d_required = (16 * T / (np.pi * tau_allow * 1e6)) ** (1 / 3) * 1000

            st.markdown("---")
            st.markdown("### 📋 设计结果")
            st.metric("所需直径", f"{d_required:.1f} mm")
            st.write(f"**建议选用直径 {int(np.ceil(d_required / 5)) * 5} mm**")

        else:  # 许用扭矩计算
            d = st.slider("轴直径 d (mm)", 10, 150, 50, 2)
            material = st.selectbox("材料", list(MATERIALS.keys()))
            mat = MATERIALS[material]
            n = st.slider("安全系数 n", 1.5, 4.0, 2.0, 0.5)
            tau_allow = mat["tau_s"] / n

            J = np.pi * (d / 1000) ** 4 / 32
            T_allow = tau_allow * 1e6 * J / (d / 2000)

            st.markdown("---")
            st.markdown("### 📋 计算结果")
            st.metric("许用扭矩", f"{T_allow:.1f} N·m")
            st.write(f"该轴可安全传递 {T_allow:.1f} N·m 的扭矩")

    with col2:
        # 扭矩-应力关系图
        T_range = np.linspace(0, T * 2 if 'T' in locals() else 4000, 50)
        if design_mode == "强度校核":
            tau_range = T_range * (d / 2000) / J / 1e6
        else:
            tau_range = T_range * (d / 2000) / J / 1e6

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=T_range, y=tau_range, mode='lines',
                                 name='应力-扭矩曲线', line=dict(color='red', width=3)))
        if design_mode == "强度校核":
            fig.add_hline(y=tau_allow, line_dash="dash", line_color="green",
                          annotation_text=f"[τ]={tau_allow:.1f}MPa")
            fig.add_vline(x=T, line_dash="dash", line_color="blue",
                          annotation_text=f"T={T}N·m")
        fig.update_layout(title="扭矩-应力关系", xaxis_title="扭矩 T (N·m)",
                          yaxis_title="切应力 τ (MPa)", height=350)
        fig = set_chinese_font(fig)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 4. 工程应用
# ============================================================
elif module == "🏗️ 工程应用":
    st.title("🏗️ 工程应用案例")

    case = st.selectbox("选择案例", [
        "汽车传动轴设计",
        "机床主轴设计",
        "风力发电机主轴",
        "机器人关节传动轴"
    ])

    if case == "汽车传动轴设计":
        st.markdown("""
        ### 🚗 汽车传动轴设计

        **工程背景**：
        某轻型卡车传动轴，传递最大扭矩 **T = 3000 N·m**，
        轴长 **L = 1.5 m**，材料 **45钢**。
        要求设计轴径，并校核强度与刚度。
        """)

        col1, col2 = st.columns(2)
        with col1:
            T = st.slider("扭矩 T (N·m)", 1000, 6000, 3000, 100)
            L = st.slider("轴长 L (m)", 0.5, 3.0, 1.5, 0.1)
            material = st.selectbox("材料", ["45钢", "40Cr钢", "Q235钢"])
            mat = MATERIALS[material]
            n = st.slider("安全系数", 1.5, 4.0, 2.0, 0.5)
            tau_allow = mat["tau_s"] / n

        with col2:
            d_required = (16 * T / (np.pi * tau_allow * 1e6)) ** (1 / 3) * 1000
            d_select = int(np.ceil(d_required / 5)) * 5

            J = np.pi * (d_select / 1000) ** 4 / 32
            tau_actual = T * (d_select / 2000) / J / 1e6
            phi = T * L / (mat["G"] * 1e9 * J) * 180 / np.pi

            st.metric("所需直径", f"{d_required:.1f} mm")
            st.metric("选用直径", f"{d_select} mm")
            st.metric("实际应力", f"{tau_actual:.2f} MPa",
                      delta=f"{tau_actual - tau_allow:.2f}" if tau_actual > tau_allow else f"裕度 {(tau_allow / tau_actual - 1) * 100:.1f}%")
            st.metric("扭转角", f"{phi:.3f}°")

            if tau_actual <= tau_allow:
                st.success("✅ 设计合格")
            else:
                st.error("❌ 应力超限，请增大直径")

    elif case == "机器人关节传动轴":
        st.markdown("""
        ### 🤖 机器人关节传动轴

        **工程背景**：
        六轴协作机器人关节传动轴，传递扭矩 **T = 50 N·m**，
        轴长 **L = 120 mm**，要求 **体积小、重量轻**。
        考虑使用 **铝合金** 或 **钛合金**。
        """)

        col1, col2 = st.columns(2)
        with col1:
            T = st.slider("扭矩 T (N·m)", 10, 200, 50, 5)
            L = st.slider("轴长 L (mm)", 50, 300, 120, 10)
            material = st.selectbox("材料", ["铝合金", "钛合金", "40Cr钢"])
            mat = MATERIALS[material]
            n = st.slider("安全系数", 1.5, 3.0, 2.0, 0.5)
            tau_allow = mat["tau_s"] / n

        with col2:
            d_required = (16 * T / (np.pi * tau_allow * 1e6)) ** (1 / 3) * 1000
            d_select = int(np.ceil(d_required / 2)) * 2

            J = np.pi * (d_select / 1000) ** 4 / 32
            tau_actual = T * (d_select / 2000) / J / 1e6
            phi = T * (L / 1000) / (mat["G"] * 1e9 * J) * 180 / np.pi

            st.metric("材料", material)
            st.metric("所需直径", f"{d_required:.1f} mm")
            st.metric("选用直径", f"{d_select} mm")
            st.metric("扭转角", f"{phi:.3f}°")

            if tau_actual <= tau_allow:
                st.success("✅ 设计合格")
            else:
                st.error("❌ 应力超限")


# ============================================================
# 5. 案例分析
# ============================================================
elif module == "📐 案例分析":
    st.title("📐 案例分析：阶梯轴扭转")

    st.markdown("""
    ### 📌 问题描述

    一根**阶梯轴**，两端受扭矩 **T**，各段直径不同。
    已知：
    - 段1: L₁ = 300 mm, d₁ = 40 mm
    - 段2: L₂ = 200 mm, d₂ = 30 mm  
    - 材料: 45钢, G = 80 GPa
    - 扭矩 T = 1000 N·m

    求：
    1. 各段的最大切应力
    2. 各段的扭转角
    3. 总扭转角
    """)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        T = st.slider("扭矩 T (N·m)", 200, 3000, 1000, 50)
        L1 = st.slider("段1长度 L₁ (mm)", 100, 600, 300, 20)
        d1 = st.slider("段1直径 d₁ (mm)", 20, 80, 40, 2)
        L2 = st.slider("段2长度 L₂ (mm)", 100, 500, 200, 20)
        d2 = st.slider("段2直径 d₂ (mm)", 15, 60, 30, 2)
        G = st.slider("剪切模量 G (GPa)", 20, 100, 80, 5)

    with col2:
        G_Pa = G * 1e9
        J1 = np.pi * (d1 / 1000) ** 4 / 32
        J2 = np.pi * (d2 / 1000) ** 4 / 32

        tau1 = T * (d1 / 2000) / J1 / 1e6
        tau2 = T * (d2 / 2000) / J2 / 1e6
        phi1 = T * (L1 / 1000) / (G_Pa * J1) * 180 / np.pi
        phi2 = T * (L2 / 1000) / (G_Pa * J2) * 180 / np.pi
        phi_total = phi1 + phi2

        st.markdown("### 📊 计算结果")

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("段1应力 τ₁", f"{tau1:.2f} MPa")
            st.metric("段2应力 τ₂", f"{tau2:.2f} MPa")
        with col_b:
            st.metric("段1扭转角 φ₁", f"{phi1:.3f}°")
            st.metric("段2扭转角 φ₂", f"{phi2:.3f}°")

        st.metric("总扭转角 φ_total", f"{phi_total:.3f}°")

        # 可视化
        x_pos = np.linspace(0, L1 + L2, 50)
        phi_dist = np.piecewise(x_pos,
                                [x_pos <= L1, x_pos > L1],
                                [lambda x: phi1 * x / L1,
                                 lambda x: phi1 + phi2 * (x - L1) / L2])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_pos, y=phi_dist, mode='lines',
                                 name='扭转角分布', line=dict(color='red', width=4),
                                 fill='tozeroy'))
        fig.add_vline(x=L1, line_dash="dash", line_color="blue",
                      annotation_text="段1→段2")
        fig.update_layout(title="扭转角沿轴分布", xaxis_title="位置 (mm)",
                          yaxis_title="扭转角 φ (°)", height=300)
        fig = set_chinese_font(fig)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 6. 应力云图
# ============================================================
elif module == "🎨 应力云图":
    st.title("🎨 扭转应力云图")
    st.markdown("可视化圆轴横截面与纵截面的应力分布")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        T = st.slider("扭矩 T (N·m)", 100, 5000, 2000, 50)
        d = st.slider("轴直径 d (mm)", 20, 120, 50, 2)
        view = st.selectbox("视图", ["横截面应力", "纵截面应力", "3D应力分布"])

    with col2:
        J = np.pi * (d / 1000) ** 4 / 32
        R = d / 2
        tau_max = T * (R / 1000) / J / 1e6

        if view == "横截面应力":
            # 横截面应力云图
            r = np.linspace(0, R, 50)
            theta = np.linspace(0, 2 * np.pi, 50)
            R_grid, Theta_grid = np.meshgrid(r, theta)
            X = R_grid * np.cos(Theta_grid)
            Y = R_grid * np.sin(Theta_grid)
            Z = tau_max * (R_grid / R)

            fig = go.Figure(data=go.Heatmap(
                z=Z,
                x=X,
                y=Y,
                colorscale='Viridis',
                colorbar=dict(title="τ (MPa)")
            ))
            fig.update_layout(title="横截面切应力分布 (沿半径线性)",
                              xaxis=dict(scaleanchor="y", scaleratio=1),
                              height=450)
            fig = set_chinese_font(fig)
            st.plotly_chart(fig, use_container_width=True)

        elif view == "纵截面应力":
            # 纵截面应力分布
            y = np.linspace(0, 100, 50)
            x = np.linspace(-R, R, 50)
            X, Y = np.meshgrid(x, y)
            Z = tau_max * (np.abs(X) / R)

            fig = go.Figure(data=go.Heatmap(
                z=Z, x=x, y=y,
                colorscale='Viridis',
                colorbar=dict(title="τ (MPa)")
            ))
            fig.update_layout(title="纵截面切应力分布", height=400)
            fig = set_chinese_font(fig)
            st.plotly_chart(fig, use_container_width=True)

        else:  # 3D
            r = np.linspace(0, R, 30)
            theta = np.linspace(0, 2 * np.pi, 30)
            R_grid, Theta_grid = np.meshgrid(r, theta)
            X = R_grid * np.cos(Theta_grid)
            Y = R_grid * np.sin(Theta_grid)
            Z = tau_max * (R_grid / R)

            fig = go.Figure(data=go.Surface(
                x=X, y=Y, z=Z,
                colorscale='Viridis'
            ))
            fig.update_layout(title="3D切应力分布 (高度=应力值)",
                              scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="τ (MPa)"),
                              height=450)
            fig = set_chinese_font(fig)
            st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 7. 3D变形动画
# ============================================================
elif module == "🔄 3D变形动画":
    st.title("🔄 3D扭转变形动画")
    st.markdown("观察圆轴在扭矩作用下的三维变形过程")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        T = st.slider("扭矩 T (N·m)", 0, 5000, 2000, 50)
        d = st.slider("轴直径 d (mm)", 20, 80, 40, 2)
        L = st.slider("轴长 L (mm)", 100, 400, 200, 10)
        G = st.slider("剪切模量 G (GPa)", 20, 100, 80, 5)

        J = np.pi * (d / 1000) ** 4 / 32
        phi = T * (L / 1000) / (G * 1e9 * J) * 180 / np.pi
        tau_max = T * (d / 2000) / J / 1e6

        st.markdown("---")
        st.metric("扭转角", f"{phi:.2f}°")
        st.metric("最大切应力", f"{tau_max:.2f} MPa")

    with col2:
        # 3D变形动画
        n_rings = 20
        n_points = 30
        z = np.linspace(0, L, n_rings)
        theta = np.linspace(0, 2 * np.pi, n_points)
        Z, Theta = np.meshgrid(z, theta)

        R = d / 2
        X = R * np.cos(Theta)
        Y = R * np.sin(Theta)

        # 变形：扭转角沿轴线性增加
        phi_rad = phi * np.pi / 180
        phi_z = phi_rad * z / L
        Theta_def = Theta + phi_z
        X_def = R * np.cos(Theta_def)
        Y_def = R * np.sin(Theta_def)

        # 原始轴（透明）
        fig = go.Figure()
        fig.add_trace(go.Surface(
            x=X, y=Y, z=Z,
            colorscale='Blues', opacity=0.3,
            name='原始', showscale=False
        ))

        # 变形轴（彩色）
        fig.add_trace(go.Surface(
            x=X_def, y=Y_def, z=Z,
            colorscale='Reds', opacity=0.8,
            name='变形', showscale=False
        ))

        # 端面标记
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[L],
            mode='markers', marker=dict(color='red', size=8),
            name='自由端'
        ))

        fig.update_layout(
            title=f"3D扭转变形 (φ = {phi:.2f}°)",
            scene=dict(
                xaxis_title="x (mm)",
                yaxis_title="y (mm)",
                zaxis_title="z (mm)",
                aspectmode='data'
            ),
            height=500,
            showlegend=True
        )
        fig = set_chinese_font(fig)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 8. 虚拟实验
# ============================================================
elif module == "🧪 虚拟实验":
    st.title("🧪 虚拟扭转实验")
    st.markdown("""
    ### 🔬 虚拟扭转实验模拟

    在虚拟实验中，你可以**实时加载**扭矩，观察轴的变形过程，
    并生成**扭矩-扭转角**曲线。
    """)

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown("### ⚙️ 实验设置")
        d_exp = st.slider("轴直径 d (mm)", 10, 80, 30, 2)
        L_exp = st.slider("标距长度 L (mm)", 50, 300, 150, 10)
        material_exp = st.selectbox("材料", list(MATERIALS.keys()))
        mat = MATERIALS[material_exp]
        G = mat["G"] * 1e9
        tau_s = mat["tau_s"] * 1e6

        J_exp = np.pi * (d_exp / 1000) ** 4 / 32
        T_max = tau_s * J_exp / (d_exp / 2000)

        load_step = st.slider("加载步长", 0.0, 1.0, 0.0, 0.05)
        T_current = load_step * T_max

        tau_curr = T_current * (d_exp / 2000) / J_exp / 1e6
        phi_curr = T_current * (L_exp / 1000) / (G * J_exp) * 180 / np.pi

        st.markdown("---")
        st.metric("当前扭矩", f"{T_current:.1f} N·m")
        st.metric("最大切应力", f"{tau_curr:.2f} MPa")
        st.metric("扭转角", f"{phi_curr:.2f}°")

        if tau_curr <= mat["tau_s"]:
            st.info(f"📌 弹性阶段 (τ ≤ {mat['tau_s']} MPa)")
        else:
            st.warning(f"⚠️ 进入塑性阶段！τ = {tau_curr:.1f} MPa > τ_s = {mat['tau_s']} MPa")

        # 扭矩-扭转角曲线
        T_range = np.linspace(0, T_max, 30)
        phi_range = T_range * (L_exp / 1000) / (G * J_exp) * 180 / np.pi
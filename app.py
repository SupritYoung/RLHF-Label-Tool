# !/usr/bin/env python3

import os
import random

import numpy as np
import pandas as pd
import streamlit as st
import json

st.set_page_config(
    page_title="Rank List Labeler",
    page_icon='📌',
    layout="wide"
)

CONFIGS = {
    'input_path': './data/input_file.json',
    'output_path': './data/output_result.tsv',  # 标注数据集的存放文件
    'rank_list_len': 4
}

if 'configs' not in st.session_state:
    st.session_state['configs'] = CONFIGS

######################## 页面配置初始化 ###########################
RANK_COLOR = [
    'red',
    'green',
    'blue',
    'orange',
    'violet'
]

######################### 页面定义区（侧边栏） ########################
st.sidebar.title('📌 RLHF Rank标注平台')
st.sidebar.markdown('''
    ```python
    用于大模型在 RLHF 阶段的数据排序标注。
    ```
''')
st.sidebar.markdown('标注思路参考自 [InstructGPT](https://arxiv.org/pdf/2203.02155.pdf) 。')
st.sidebar.markdown('项目 [github地址](https://github.com/SupritYoung/rlhf_label_tool). I need your ⭐️.')

st.sidebar.header('📢 注意事项')
st.sidebar.write('1. 需要预先构建好数据文件，格式参见 input_file.json。')
st.sidebar.write('2. 将构造好的数据地址替换配置中的 output_path。')
st.sidebar.write('3. 可以跳转标注，重复标注会覆盖，但建议按顺序标注。')

st.sidebar.header('⚙️ Model Config')
st.sidebar.write('当前标注配置（可在源码中修改）：')
st.sidebar.write(st.session_state['configs'])

label_tab, dataset_tab = st.tabs(['Label', 'Dataset'])

######################### 页面定义区（标注页面） ########################
with label_tab:
    with st.expander('🔍 Setting Prompts', expanded=True):
        with open(CONFIGS['input_path'], 'r') as f:
            data = json.load(f)

        query_ids = list(data.keys())
        query_index = st.empty()
        query_index_number = query_index.number_input('当前 query 编号（点击右边的➕➖前后跳转）：', min_value=0,
                                                      max_value=len(query_ids) - 1, value=0)

        current_query_id = query_ids[query_index_number]
        current_query = data[current_query_id]['query']
        current_history = data[current_query_id]['history']

        st.markdown(f'**Query:** {current_query}')
        st.markdown('**History:**')
        for history_item in current_history:
            st.write(f'- {history_item[0]}')
            st.write(f'  {history_item[1]}')

        # 排序功能
    with st.expander('💡 Generate Results', expanded=True):
        rank_results = []
        for i in range(CONFIGS['rank_list_len']):
            # st.write(f'**Response {i + 1}:**，请标注其排名')
            response_text = data[current_query_id][f'response_{i}']
            rank = st.selectbox(f'请标注回答 {i + 1} 的排名', [-1, 1, 2, 3, 4],
                                help='为当前 Response 选择排名，回答质量越好，排名越靠前。（-1代表当前句子暂未设置排名）')

            conflict_index = next((idx + 1 for idx, r in enumerate(rank_results) if r == rank), None)
            if conflict_index is not None and rank != -1:
                st.info(
                    f'当前排名[{rank}]已经被句子[{conflict_index}]占用，请先将占用排名的句子置为-1再为当前句子分配该排名。')
            else:
                rank_results.append(rank)

            st.markdown(f"<span style='color:{RANK_COLOR[i]}'>{response_text}</span>", unsafe_allow_html=True)
            st.write(f'当前排名：**{rank}**')
            # st.write('---')

        # 排序存储功能
        if -1 not in rank_results:
            save_button = st.button('存储当前排序')
            if save_button:
                dataset_file = CONFIGS['output_path']
                df = pd.read_csv(dataset_file, delimiter='\t', dtype=str)
                # print(df)
                existing_ids = df['id'].tolist()

                rank_texts = [data[current_query_id][f'response_{rank - 1}'] for rank in rank_results]
                line = [current_query_id, current_query, current_history] + rank_texts
                new_row = pd.DataFrame([line], columns=df.columns)

                if current_query_id in existing_ids:
                    df = df[df['id'] != current_query_id]  # 删除已存在的行

                df = pd.concat([df, new_row], ignore_index=True)  # 追加新行

                df.to_csv(dataset_file, index=False, sep='\t')  # 保存到文件

                query_index_number += 1
                if query_index_number >= len(query_ids):
                    st.write('已完成所有查询的标注')
                    st.stop()

                query_index.number_input('当前是第几个query', min_value=0, max_value=len(query_ids) - 1,
                                         value=query_index_number)

                st.success(f'{current_query_id} 数据保存完成')
        else:
            st.error('请完成排序后再存储！', icon='🚨')

    # with st.expander('🥇 Rank Results', expanded=True):
    #     columns = st.columns([1] * CONFIGS['rank_list_len'])
    #     for i, c in enumerate(columns):
    #         with c:
    #             st.write(f'Rank {i+1}：')
    #             if i + 1 in rank_results:
    #                 color = RANK_COLOR[rank_results.index(i+1)] if rank_results.index(i+1) < len(RANK_COLOR) else 'white'
    #                 st.markdown(f":{color}[{st.session_state['current_results'][rank_results.index(i+1)]}]")

######################### 页面定义区（数据集页面） #######################
with dataset_tab:
    dataset_file = CONFIGS['output_path']
    df = pd.read_csv(dataset_file, delimiter='\t', dtype=str)

    st.dataframe(df)

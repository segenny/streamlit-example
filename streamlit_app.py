from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

CHOSUNG_dict = {'ㄱ':2, 'ㄲ':4, 'ㄴ':2, 'ㄷ':3, 'ㄸ':6, 'ㄹ':5, 'ㅁ':4, 'ㅂ':4, 'ㅃ':8, 'ㅅ':2, 'ㅆ':4, 'ㅇ':1, 'ㅈ':3, 'ㅉ':6, 'ㅊ':4, 'ㅋ':3, 'ㅌ':4, 'ㅍ':4, 'ㅎ':3}
JUNGSUNG_dict = {'ㅏ':2, 'ㅐ':3, 'ㅑ':3, 'ㅒ':4, 'ㅓ':2, 'ㅔ':3, 'ㅕ':3, 'ㅖ':4, 'ㅗ':2, 'ㅘ':4, 'ㅙ':5, 'ㅚ':3, 'ㅛ':3, 'ㅜ':2, 'ㅝ':4, 'ㅞ':5, 'ㅟ':3, 'ㅠ':3, 'ㅡ':1, 'ㅢ':2, 'ㅣ':1}
JONGSUNG = {' ':0, 'ㄱ':2, 'ㄲ':4, 'ㄳ':4, 'ㄴ':2, 'ㄵ':5, 'ㄶ':5, 'ㄷ':3, 'ㄹ':5, 'ㄺ':7, 'ㄻ':9, 'ㄼ':9, 'ㄽ':7, 'ㄾ':9, 'ㄿ':9, 'ㅀ':8, 'ㅁ':4, 'ㅂ':4, 'ㅄ':6, 'ㅅ':2, 'ㅆ':4, 'ㅇ':1, 'ㅈ':3, 'ㅊ':4, 'ㅋ':3, 'ㅌ':4, 'ㅍ':4, 'ㅎ':3}


def korean_to_be_englished(korean_word):
    r_lst = []
    for w in list(korean_word.strip()):
        # 영어인 경우 구분해서 작성함.
        if '가' <= w <= '힣':
            # 588개 마다 초성이 바뀜.
            ch1 = (ord(w) - ord('가')) // 588
            # 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
            # 각 문자에 해당하는 값을 가져와 숫자로 변환하여 리스트에 추가
            r_lst.append([CHOSUNG_dict[CHOSUNG_LIST[ch1]], JUNGSUNG_dict[JUNGSUNG_LIST[ch2]], JONGSUNG[JONGSUNG_LIST[ch3]]])
        else:
            r_lst.append([w])
    return r_lst

def sum_lists(lists):
    result = []
    for sublist in lists:
        total = sum(sublist)
        result.append(total)
    return result


def combine_lists(list1, list2):
    combined_list = []
    for i in range(len(list1)):
        combined_list.append(list1[i])
        combined_list.append(list2[i])
    return combined_list

def calculate_digit_sum(num_list):
    new_list = []
    for i in range(len(num_list) - 1):
        digit_sum = (num_list[i] + num_list[i + 1]) % 10
        new_list.append(digit_sum)
    return new_list

def iloveyou(이름1, 이름2):
    result_msg = ""
    result_msg2 = ""
    # st.write(이름1, ' -> ', 이름2)
    result_msg += f"{이름1}, ' -> ', {이름2}\n"
    이름_1 = sum_lists(korean_to_be_englished(이름1))
    이름_2 = sum_lists(korean_to_be_englished(이름2))

    result = combine_lists(이름_1, 이름_2)
    result_msg += f"{이름1[0]},{이름2[0]},{이름1[1]},{이름2[1]},{이름1[2]},{이름2[2]}\n"
    # st.write(이름1[0],이름2[0],이름1[1],이름2[1],이름1[2],이름2[2])
    # st.write(str(result))
    result_msg += str(result)+"\n"


    # 5개의 숫자로 리스트 만들기
    first_step = calculate_digit_sum(result)
    # st.code(first_step)
    result_msg += str(first_step)+"\n"

    while len(first_step) >= 3:
        first_step = calculate_digit_sum(first_step)
        # st.code(first_step)
        result_msg += str(first_step)+"\n"

    # 최종 결과를 두 자리 숫자로 만들기
    final_result = str(first_step[0]) + str(first_step[1])

    # st.code(이름1 + ' -> ' + 이름2 + ' = ' + final_result)
    result_msg += f"{이름1} + ' -> ' + {이름2} + ' = ' + {final_result}\n"

    st.code(result_msg)
    

    # st.code(이름2, ' -> ', 이름1)
    result_msg2 += f"{이름2}, ' -> ', {이름1}\n"
    result = combine_lists(이름_2, 이름_1)

    # st.code(이름2[0],이름1[0],이름2[1],이름1[1],이름2[2],이름1[2])
    result_msg2 += f"{이름2[0]},{이름1[0]},{이름2[1]},{이름1[1]},{이름2[2]},{이름1[2]}\n"
    result_msg2 += str(result)+"\n"
    # st.code(result)


    first_step = calculate_digit_sum(result)
    # st.code(first_step)
    result_msg2 += str(first_step)+"\n"

    while len(first_step) >= 3:
        first_step = calculate_digit_sum(first_step)
        # st.code(first_step)
        result_msg2 += str(first_step)+"\n"

    # 최종 결과를 두 자리 숫자로 만들기
    final_result = str(first_step[0]) + str(first_step[1])

    st.code(이름2 + ' -> ' + 이름1 + ' = ' + final_result)
    result_msg2 += f"{이름2} + ' -> ' + {이름1} + ' = ' + {final_result}\n"
    st.code(result_msg2)


# Streamlit 앱 제목 설정
st.title('간단한 덧셈 계산기')

# 입력창 2개 추가
number1 = st.text_input('첫 번째 숫자 입력')
number2 = st.text_input('두 번째 숫자 입력')

# 실행 버튼 클릭 여부 확인
if st.button('계산'):
    # 입력된 숫자를 더하고 결과 출력
    iloveyou(number1, number2)

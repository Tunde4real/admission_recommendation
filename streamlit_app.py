# -- coding: utf-8 -
# written by Ibrahim Aderinto


import pandas as pd
import streamlit as st
from engine import recommend


def main():
    header = st.container()
    motivation = st.container()
    recommendation = st.container()
    result = st.container()

    with header:
        # you only use the title once
        st.markdown("<h1 style='text-align: center;'>Admission Recommendation System for Pre-Tertiary Institution Candidates in Nigeria</h1>", unsafe_allow_html=True)
        
        # add some space
        st.text('')
        st.text('')
        st.text('')

    with motivation:
        with open('motivation.txt') as file:
            #motivation = file.read()
            motivation = file.read()
        st.markdown(f"<p style='text-align:center; font-family:\"Source Code Pro\", monospace;;'>{motivation}</p>", unsafe_allow_html=True)
        # st.text(motivation)

        # add some space
        st.text('')
        st.text('')

    with recommendation:
        st.subheader('Recommendation Engine')
        waec_subjects = pd.read_csv('subjects.csv', index_col='subjects')
        st.text("Select your waec subjects and their corresponding grades. Enter at least five\nsubjects and grades")
        subject, grade = st.columns(2)
        subjects, grades = [], []

        for i in range(1,10):
            subject_ = subject.selectbox(f'Subject {i}', options=[''] + sorted(list(waec_subjects.index)), index=0, key=f'00{i}')
            grade_ = grade.selectbox(f'Grade {i}', options=['', 'a1', 'b2', 'b3', 'c4', 'c5', 'c6', 'd7', 'd8', 'f9'], index=0, key=f'00{i}0')
            if subject_ != '':
                subjects += [subject_]
            if grade_ != '':
                grades += [grade_]

        # add some space
        st.text('')
        st.text('')

        box1, box2 = st.columns(2)
        jamb_subjects, state_of_origin = box1.container(), box1.container()
        jamb_subjects = jamb_subjects.multiselect(f'Jamb Subjects', options=sorted(list(waec_subjects.index)))
        state_of_origin = state_of_origin.selectbox(f'Select your state of origin', options=['', 'Lagos', 'Ogun', 'Osun', 'Ondo', 'Oyo', 'Ekiti'])
        state_of_origin = state_of_origin.lower()

        jamb_score, post_jamb_score = box2.container(), box2.container()
        jamb_score = jamb_score.number_input('Enter your jamb score if any')
        post_jamb_score = post_jamb_score.number_input(r'Enter your post jamb score if any, in % of 100')
        jamb_score, post_jamb_score = int(jamb_score), int(post_jamb_score)
        
        # add some space
        st.text('')
        st.text('')

        interests_df = pd.read_csv('interests.csv')
        interests_arr = list(interests_df['characteristics'])
        interests_options = []
        for i in interests_arr:
            interests_options += i.split(' ')
        interests_options = list(set(interests_options))

        interests = st.multiselect('Select your interests', options = interests_options)

        course, university = st.columns(2)

        courses = ['', 'accountancy', 'architecture', 'biochemistry', 'business administration', 'estate management',\
            'civil engineering', 'chemical engineering', 'computer engineering', 'computer science', 'electrical engineering',\
            'law', 'marketing', 'medicine and surgery', 'mass communication', 'nursing', 'pharmacy', 'theatre arts',
            ]
        course = course.selectbox('Select your intended/chosen course', options=courses)

        universities = {
                        'oau' : 'Obafemi Awolowo University',
                        'ui' : 'University of Ibadan',
                        'funaab' : 'Federal University of Agriculture, Abeokuta',
                        'futa' : 'Federal University of Technology, Akure',
                        'unilag' : 'University of Lagos',
                        'aaua' : 'Adeleke Ajasin University, Akungba',
                        'eksu' : 'Ekiti State University',
                        'lasu' : 'Lagos State University',
                        'lautech' : 'Ladoke Akintola University of Technology',
                        'oou' : 'Olabisi Onabanjo University',
                        'abuad' : 'Afe Babalola University',
                        'aue' : 'Adeleke University',
                        'babcock' : 'Babcock University',
                        'bowen' : 'Bowen University',
                        'covenant' : 'Covenant University',
                        'ede' : 'Federal Polytechnic, Ede',
                        'ibadan' : 'The Polytechnic Ibadan',
                        'ilaro' : 'Federal Polytechnic, Ilaro',
                        'laspotech' : 'Lagos State Polytechnic, Ikorodu',
                        'yaba' : 'Yaba College of Technology',
                        'adeyemi_ce' : 'Adeyemi College of Education, Ondo',
                        'emmanuel_a_ce' : 'Emmanuel Ayanlade College of Education',
                        'fce_abeokuta' : 'Federal College of Education, Abeokuta',
                        'fce_oyo' : 'Federal College of Education, Oyo'
                        }
        unis = [universities[i] for i in universities]
        university = university.selectbox('Select your intended/chosen university', options=[''] + unis)
        # add some space
        st.text('')
        st.text('')

        def get_recommendation():
            '''
                A callback function to call the recommendation engine and write recommendation to app
            '''

            # validate waec subjects
            if len(subjects) < 5:
                recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You inputed less than 5 waec subjects</h3>", unsafe_allow_html=True)
                return False
            elif len(grades) > len(subjects):
                recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You're missing some waec subjects</h3>", unsafe_allow_html=True)
                return False
            elif len(grades) < len(subjects):
                recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You're missing some waec grades</h3>", unsafe_allow_html=True)
                return False
            elif len(subjects) != len(set(subjects)):
                recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You inputed a waec subject more than once</h3>", unsafe_allow_html=True)
                return False
            
            sub_grades = ''
            for index, sub in enumerate(subjects):
                short_form = waec_subjects.loc[sub][0]
                sub_grades += f'{short_form} {grades[index]}, '
            sub_grades = sub_grades[:-2]

            # validate jamb subjects
            if len(jamb_subjects) != 0 and jamb_score == 0.0:
                recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You need to input a jamb score</h3>", unsafe_allow_html=True)
                return False

            elif len(jamb_subjects) > 4 and jamb_score!=0.0:
                recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You inputed more than 4 jamb subjects</h3>", unsafe_allow_html=True)
                return False

            elif len(jamb_subjects) < 4 and jamb_score!=0.0:
                recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You inputed less than 4 jamb subjects</h3>", unsafe_allow_html=True)
                return False
            
            # validate jamb score and post jamb score
            if post_jamb_score!=0 and jamb_score==0:
                recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You need to input jamb score</h3>", unsafe_allow_html=True)
                return False

            jamb_subs = ''
            for sub in jamb_subjects:
                short_form = waec_subjects.loc[sub][0]
                jamb_subs += f'{short_form} '
            jamb_subs = jamb_subs[:-1]

            university_ = university[:]
            for i in universities:
                if universities[i] == university_:
                    university_ = i
            
            # validate university, course and post jamb score
            # if university_!='' and post_jamb_score==0:
            #     recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You need to input post jamb score</h3>", unsafe_allow_html=True)
            #     return False
            # elif course!='' and post_jamb_score==0:
            #     recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You need to input post jamb score</h3>", unsafe_allow_html=True)
            #     return False

            if post_jamb_score!=0 and course=='':
                recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You need to input chosen course</h3>", unsafe_allow_html=True)
                return False
            elif post_jamb_score!=0 and university_=='':
                recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You need to input chosen university</h3>", unsafe_allow_html=True)
                return False
            
            if jamb_score > 400:
                recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You inputed an invalid jamb score</h3>", unsafe_allow_html=True)
                return False
            elif post_jamb_score > 100:
                recommendation.markdown("<h3 style='text-align: center; color: red;'>!! You inputed an invalid post jamb score</h3>", unsafe_allow_html=True)
                return False

            reco = recommend(sub_grades, jamb_subs, jamb_score, post_jamb_score, course, university_, state_of_origin, interests)
            reco = dict(sorted(reco.items(), key=lambda item: item[1])[::-1])
            
            for index,i in enumerate(reco):
                key = i.split('-')
                key = [i.strip() for i in key]
                if index < 10:
                    text = f"{universities[key[0]]} -- {key[1][0].upper()}{key[1][1:]}"
                    recommendation.markdown(f"<h4 style='text-align: center; color: #d4cce6;'>{text}</h4>", unsafe_allow_html=True)
                else:
                    break

            if len(reco) == 0:
                recommendation.markdown("<h3 style='text-align: center; color: red;'>!! No recommendation at this time, Try again with more data</h3>", unsafe_allow_html=True)
                return False

        st.button('Get Recommendation', on_click=get_recommendation)


if __name__=='__main__':
    main()

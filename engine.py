# -- coding: utf-8 -
# written by Ibrahim Aderinto - ib4real914@gmail.com

# import system libraries
import os
import copy
from glob import glob

# 3rd party modules
import pandas as pd


def waec_score(grades):
    ''' A function to calculate waec score given a list of grades that are 5 in lenght.

        :arguments:
            grades - a list of grades
        
        :returns:
            the percentage score
    '''

    grades_ = {'a1':8, 'b2':7, 'b3':6, 'c4':5, 'c5':4, 'c6':3, 'd7':2, 'd8':1, 'f9':0}
    s = 0
    for i in grades:
        s += grades_[i]
    return (s/40)*100


def highest_sub(subjects, real_subs, sub_grades):
    ''''
        A function to get the subject with the highest grade

        :arguments:
            subjects - the list of subjects to get highest graded subject from
            read_subs - subjects already selected from student's waec subjects
            sub_grades - a dictionary of subjects and grades
        
        :returns:
            sub - highest graded subject
    '''

    subjects_ = subjects[:]
    sub_grades_ = copy.deepcopy(sub_grades)
    for sub in real_subs:
        if sub in subjects:
            subjects_.remove(sub)
            del(sub_grades_[sub])
    
    grades_ = {}
    for i in  sub_grades_:
        grades_[sub_grades_[i]] = i
    
    grades = ['a1', 'b2', 'b3', 'c4', 'c5', 'c6', 'd7', 'd8', 'f9']
    for grade in grades:
        if grade in grades_:
            sub = grades_[grade]
            if sub in subjects_:
                return [sub]
    
    return []    


def get_institutions(course, waec_subs, jamb_subs):
    ''' A function to check the database and return all the courses a student is qualified to take

        :arguents:
            course - a course of study
            subjects - an array in the form passed_waec_subjects in the form ['sub grade', 'sub grade' ...]

        :returns:
            arr - an array that contains a list of institutions qualified for
    '''

    jamb_subs = jamb_subs.split()
    waec_subs = [i.split(' ') for i in waec_subs]
    grades = [i[1] for i in waec_subs]
    waec_subs = [i[0] for i in waec_subs]

    sub_grades = {}     # a dictionary of subjects mapped to corresponding grades

    for i in range(len(waec_subs)):
        sub_grades[waec_subs[i]] = grades[i]

    science = ['phy', 'chem', 'fur_math', 'bio', 'geo', 'agric', 'pe', 'he', 'am']
    soc_science = ['comm', 'accnt', 'econs', 'govt', 'geo']
    art = ['lit_in_eng', 'his', 'fn', 'igbo', 'hausa', 'yor', 'govt', 'irs', 'crs']

    arr = {}    # a dictionary in the form {'uni -- course:score', ...} to be returned
    files = glob('courses\*')
    print('\nfiles', files)
    # files = ['courses/'+i for i in os.listdir('courses')]

    # for folder in courses folder
    for i in files:
        csv_files = glob(f'{i}\*')          # does the same thing as the line below
        print('\ncsv files', csv_files)
        # csv_files = [i+'/'+j for j in os.listdir(i)]

        # for file in the folder
        for file in csv_files:
            df = pd.read_csv(file, index_col='courses')

            # check if course is listed
            try:
                row = df.loc[course]
            except:
                continue

            if type(row[0]) != str:
                continue
            waec_subjects = row[0].split(' ')
            jamb_subjects = row[1].split(' ')
            real_subs = []
            
            # for every subject in waec subjects required to study the course
            for sub in waec_subjects:
                # if subject in waec subjects of student
                if sub in waec_subs:
                    real_subs += [sub]
                    continue
                   
                # if subject is stated as any1
                elif sub == 'any1':
                    real_subs += highest_sub(waec_subs, real_subs, sub_grades)
                    continue

                # if subject is listed as any1 of a group of subjects
                elif 'any1(' in sub:
                    sub = sub.replace('any1(', '')
                    sub = sub[:-1]
                    subs = sub.split('-')
                    common_subs = []

                    for ele in subs:
                        if r'/' in ele:
                            options = ele.split(r'/')
                            real_options = [i for i in options if i in waec_subs]
                            common_subs += highest_sub(real_options, real_subs, sub_grades)
                    
                    common_subs += list(set(subs).intersection(set(waec_subs)))
                    if len(common_subs) >= 1:
                        real_subs += highest_sub(waec_subs, real_subs, sub_grades)
                    else:
                        break
                
                elif r'any2(' in sub:
                    sub = sub.replace('any2(', '')
                    sub = sub[:-1]
                    subs = sub.split('-')
                    common_subs = []

                    for ele in subs:
                        if r'/' in ele:
                            options = ele.split(r'/')
                            real_options = [j for j in options if j in waec_subs]
                            common_subs += highest_sub(real_options, real_subs, sub_grades)

                    common_subs += list(set(subs).intersection(set(waec_subs)))
                    if len(common_subs) >= 2:
                        real_subs += highest_sub(waec_subs, real_subs, sub_grades)
                        real_subs += highest_sub(waec_subs, real_subs, sub_grades)
                    else:
                        break
                
                # if there are multiple options in the form sub/sub e.g goe/phy
                elif r'/' in sub:
                    options = sub.split(r'/')
                    real_options = [i for i in options if i in waec_subs]
                    real_subs += highest_sub(real_options, real_subs, sub_grades)
                
                elif sub=='any_sc':
                    common_subs = list(set(science).intersection(set(waec_subs)))
                    if len(common_subs) >= 1:
                        real_subs += highest_sub(waec_subs, real_subs, sub_grades)
                    else:
                        break
                
                elif sub=='any_soc_sc':
                    common_subs = list(set(soc_science).intersection(set(waec_subs)))
                    if len(common_subs) >= 1:
                        real_subs += highest_sub(waec_subs, real_subs, sub_grades)
                    else:
                        break
                
                elif sub=='any_art':
                    common_subs = list(set(art).intersection(set(waec_subs)))
                    if len(common_subs) >= 1:
                        real_subs += highest_sub(waec_subs, real_subs, sub_grades)
                    else:
                        break
                
                # if student misses one of the required subjects
                elif sub not in waec_subs:
                    break
            
            real_jamb_subs = []
            for sub in jamb_subjects:
                # if subject in waec subjects of student
                if sub in jamb_subs:
                    real_jamb_subs += [sub]
                    continue
                   
                # if subject is stated as any1
                elif sub == 'any1':
                    real_jamb_subs += ['any1']
                    continue

                # if subject is listed as any1 of a group of subjects
                elif 'any1(' in sub:
                    sub = sub.replace('any1(', '')
                    sub = sub[:-1]
                    subs = sub.split('-')
                    common_subs = []

                    for ele in subs:
                        if r'/' in ele:
                            options = ele.split(r'/')
                            real_options = [i for i in options if i in jamb_subs]
                            common_subs += real_options
                    
                    common_subs += list(set(subs).intersection(set(jamb_subs)))
                    if len(common_subs) >= 1:
                        for i in common_subs:
                            if i not in real_jamb_subs:
                                real_jamb_subs += i
                                break
                    else:
                        break
                
                elif r'any2(' in sub:
                    sub = sub.replace('any2(', '')
                    sub = sub[:-1]
                    subs = sub.split('-')
                    common_subs = []

                    for ele in subs:
                        if r'/' in ele:
                            options = ele.split(r'/')
                            real_options = [j for j in options if j in jamb_subs]
                            common_subs += real_options

                    common_subs += list(set(subs).intersection(set(waec_subs)))
                    if len(common_subs) >= 2:
                        h = 0
                        for i in common_subs:
                            if i not in real_jamb_subs:
                                real_jamb_subs += i
                                h += 1
                                if h==2:
                                    break
                    else:
                        break
                
                # if there are multiple options in the form sub/sub e.g goe/phy
                elif r'/' in sub:
                    options = sub.split(r'/')
                    real_options = [i for i in options if i in jamb_subs]
                    if len(real_options) >= 1:
                        for option in real_options:
                            if option not in real_jamb_subs:
                                real_jamb_subs += [real_options[0]]
                                break
                    else:
                        break
                
                elif sub=='any_sc':
                    common_subs = list(set(science).intersection(set(jamb_subs)))
                    if len(common_subs) >= 1:
                        for a in common_subs:
                            if a not in real_jamb_subs:
                                real_jamb_subs += [a]
                                break
                    else:
                        break
                
                elif sub=='any_soc_sc':
                    common_subs = list(set(soc_science).intersection(set(jamb_subs)))
                    if len(common_subs) >= 1:
                        for a in common_subs:
                            if a not in real_jamb_subs:
                                real_jamb_subs += [a]
                                break
                    else:
                        break
                
                elif sub=='any_art':
                    common_subs = list(set(art).intersection(set(jamb_subs)))
                    if len(common_subs) >= 1:
                        for a in common_subs:
                            if a not in real_jamb_subs:
                                real_jamb_subs += [a]
                                break
                    else:
                        break
                
                # if student misses one of the required subjects
                elif sub not in jamb_subs:
                    break

            # if student meet all subject requirements
            if len(real_subs) >= 5 and (len(real_jamb_subs) == 4 or real_jamb_subs == []):
                grades = []
                for i in real_subs:
                    grades += [sub_grades[i]]
                score = waec_score(grades)
                if score > 50:
                    file_split = file.split('\\')
                    print('\n1 file split', file_split)
                    arr[file_split[-1][:-4] + f' -- {course}'] = score
            
            elif len(real_subs) == 4 and (len(real_jamb_subs) == 4 or real_jamb_subs == []):
                file_split = file.split('\\')
                print('\nFile split: ', file_split, '\n')
                if file_split[1]=='colleges':
                    grades = []
                    for i in real_subs:
                        grades += [sub_grades[i]]
                    score = waec_score(grades)
                    if score > 50:
                        arr[file.split('/')[-1][:-4] + f' -- {course}'] = score
    return arr


def normalize(variable):
    '''
        A function to turn a string integer into an integer or 0 if string is empty

        :arguments:
            variable: the string integer to convert

        :returns:
            Nonw
    '''

    if variable == '':
        return 0
    else:
        return int(variable)


def institutions(course, subjects, jamb_subjects, char):
    '''
        A function to get all possible institutions a student is qualified for given intended course and interests
        of the student

        :arguments:
            course - desired course by student
            subjects - subjects took in waec
            char - students' interests and abilities

        :returns:
            hash_arr - an array in the form {'uni -- course':weight} for all courses and qualified unis
    '''

    courses_similar = {
        'biology':['biochemistry', 'medicine and surgery', 'nursing', 'pharmacy'],
        'business education': ['accountancy', 'business administration', 'estate management', 'marketing'],
        'computer science education': ['architecture', 'computer science', 'computer engineering', 'electrical engineering', 'chemical engineering', 'civil engineering'],
        'fine and applied arts': ['theatre arts', 'mass communication', 'law']
    }

    subjects = subjects.split(', ')

    # If student didn't input any course
    if course!='':
        hash_arr = get_institutions(course, subjects, jamb_subjects)
    else:
        hash_arr = {}

    # read csv of courses with respective interest attributes
    data = pd.read_csv('interests.csv')
    courses = list(data['courses'])     # get all courses in data
    chars = list(data['characteristics'])   # get all corresponsing interest attributes
    
    # generate a dictionary in the form {course:[interests attributes], ...}
    data_dic = {}
    for i in range(len(courses)):
        data_dic[courses[i].lower()] = chars[i].lower().split(' ')

    # get courses with similar interests and abilities
    similar_courses = []
    for i in data_dic:
        x = len(set(char).intersection(set(data_dic[i])))
        y = len(data_dic[i])
        if ((x/y) * 100) >= 70:
            similar_courses += [i]
    
    # for every course in similar courses recommended based on interests and abilities:
    # get us the similar course offered in the colleges of education.
    for i in courses_similar:
        similar_courses_copy = similar_courses[:] + [course]
        for j in similar_courses_copy:
            if j in courses_similar[i]:
                similar_courses += [i]
    
    # for course in similar_courses, get institutions qualified for, and their respective weights
    similar_courses = set(similar_courses)
    for ele in similar_courses:
        new_recomm = get_institutions(ele, subjects, jamb_subjects)
        for i in new_recomm:
            if i not in hash_arr:
                hash_arr[i] = new_recomm[i]
            else:
                new_value = new_recomm[i]
                old_value = hash_arr[i]
                if new_value > old_value:
                    hash_arr[i] = new_value

    return hash_arr


def recommend(waec_subjects, jamb_subjects, jamb_score, post_jamb, course, uni, state_of_origin, personal_interests):
    '''
        A function that serves as the recommendation engine.

        :arguments: compulsory fields starts with *
            *waec_subjects - student's waec subject.
            *state_of_origin - student's state of origin.
            *personal_interests - student's interests like science, mathematics.
            jamb_subjects - student's jamb subject if any.
            jamb_score - student's jamb score if any.
            post_jamb - student's post jamb score if any. All other optional inputs becomes compulsory if this
                        is inputed.
            course - chosen/intended course of study.
            uni - chosen/intended university of study.

        :returns:
            recommendation - a dictionary in the form {'uni -- course':weight, ...}.
    '''

    recommendation = {}
    jamb_score = normalize(jamb_score)
    post_jamb = normalize(post_jamb)


    def get_soo(institution, state):
        '''
            A simple function to fetch state of origin weight

            :arguments:
                institution - the institution involved
                state - the state of the student
            
            :returns:
                10 or 0
        '''
        all_states ={
        'ogun' : ['funaab', 'oou', 'ilaro', 'fce_aboekuta'],
        'ekiti' : ['futa', 'eksu'],
        'osun' : ['oau', 'ede'],
        'oyo' : ['ui', 'lautech', 'ibadan', 'fce_oyo'],
        'lagos' : ['unilag', 'lasu', 'yaba', 'laspotech', 'fce_akoka'],
        'ondo' : ['aaua', 'adeyemi_ce']
        }
        for state_ in all_states:
            if institution in all_states[state_] and state_==state:
                return 10
        return 0
    

    universities = ['funaab', 'oou', 'futa', 'eksu', 'oau', 'ui', 'lautech', 'unilag', 'lasu', 'aaua', 'abuad',\
                    'aue', 'babcock', 'bowen', 'covenant']
    polytechnics = ['ede', 'ibadan', 'ilaro', 'laspotech', 'yaba']
    colleges = ['adeyemi', 'emmanuel_a_ce', 'fce_abeokuta', 'fce_akoka', 'fce_oyo']

    post_jamb_data = pd.read_csv('cutoff.csv', index_col='courses')
    waec_recommendation = institutions(course, waec_subjects, jamb_subjects, personal_interests)
    
    for reco in waec_recommendation:
        reco_uni = reco.split('--')[0].strip()
        reco_course = reco.split('--')[1].strip()
        # turn waec to a number in 50%
        waec_weight = (waec_recommendation[reco]/100) * 50

        institution = reco[:reco.index('-')].strip()
        course_ = reco[len(institution)+3:].strip()
        soo_weight = get_soo(institution, state_of_origin)

        jamb_weight = 0
        if jamb_score > 0 and jamb_score < 100:
            return {}
        elif jamb_score > 100:
            if institution in universities:
                if jamb_score>=160:
                    jamb_weight = 5 + ((jamb_score-160)/240) * 15
                else:
                    # jamb_weight = 5*(1 - jamb_score/160)
                    continue
            elif institution in polytechnics:
                if jamb_score>=120:
                    jamb_weight = 5 + ((jamb_score - 120)/280) * 15
                else:
                    continue
            elif institution in colleges:
                if jamb_score>=100:
                    jamb_weight = 5 + ((jamb_score - 100)/300) * 15
        
        post_jamb_weight = 0
        # if there's a post jamb score
        if post_jamb != 0:
            # if course recommended is applicant's intended course
            if reco_course == course and reco_uni==uni:
                try:
                    row = post_jamb_data.loc[course_]
                    score = row[uni]
                    try:
                        score = int(score)
                        assert post_jamb >= score
                        post_jamb_weight = 5 + ((post_jamb - score)/(100-post_jamb))*15
                    except Exception as e:
                        continue
                except:
                    pass
        
        final_weight = waec_weight + soo_weight + jamb_weight + post_jamb_weight
        # If no jamb and post jamb score
        if jamb_weight == 0 and post_jamb_weight == 0:
            final_weight = (final_weight/60)*100

        # if there's one of jamb or post jamb score
        elif jamb_weight == 0 or post_jamb_weight==0:
            final_weight = (final_weight/80)*100
        
        # if overall weight is greater than 70%
        if final_weight >= 60:
            recommendation[f"{institution} - {course_}"] = round(final_weight, 2)
    return recommendation


if __name__ == "__main__":
    # print(recommend('math a1, eng c6, phy b3, chem c4, bio c5, geo a1, agric b2, econs b3, fur_math c4', 'eng bio chem phy', 167, 56, 'estate management', \
    # 'ui', 'ogun', ['science', 'math', 'good-memory', 'patience', 'business-oriented', 'knowledgeable', 'caring', 'empathy', 'communication', 'stamina', 'detail-oriented', 'altruism', 'creativity', 'teamwork']))
    pass
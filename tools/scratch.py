from antipetros_discordbot.utility.gidtools_functions import loadjson, writejson


data_file = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\antipetros_discordbot\init_userdata\data_pack\fixed_data\converted_faq_list.json"

faq_data = loadjson(data_file)
_new_faq_data = []
for faq_num, faq_text in faq_data.items():
    _, faq_text = faq_text.split(':regional_indicator_q:')
    faq_question, faq_answer = faq_text.split(':regional_indicator_a:')
    faq_question = faq_question.strip('\n').strip()
    faq_answer = faq_answer.strip('\n').strip()
    faq_num = int(faq_num.replace('FAQ No ', '').strip())
    _new_faq_data.append({'number': faq_num, 'question': faq_question, 'answer': faq_answer})

writejson(_new_faq_data, 'faq_data.json')

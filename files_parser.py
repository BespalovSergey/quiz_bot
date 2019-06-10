import os

def get_data(file_folder):
  file_list = os.listdir(file_folder)
  questions = {}
  answers = {}

  for name in file_list:
    with open('{}/{}'.format(file_folder,name) ,'r',encoding = 'KOI8-R') as my_file:
      file_content = my_file.read()
      file_content = file_content.split('\n\n\n')

      for  i,content in enumerate( file_content):
        if content[:7] != 'Вопрос' :
         file_content[i] = file_content[i][file_content[i].find('Вопрос '):]

      for item in file_content[:-1]:
        item = item.split('\nОтвет')

        if(len(item)<2):
          continue
          
        question =   item[0][item[0].find('\n')+1:].strip()
        answer = item[1][item[1].find('\n'):item[1].find('\n\n')].strip()
        questions[question] =  answer
        
  return questions

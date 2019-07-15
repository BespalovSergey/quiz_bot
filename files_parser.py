import os

def get_questions(file_folder):
  file_list = os.listdir(file_folder)
  questions = []
  
  

  for name in file_list:
    with open('{}/{}'.format(file_folder,name) ,'r',encoding = 'KOI8-R') as my_file:
      file_content = my_file.read()
      lines = file_content.split('\n\n\n')

      for  i,line in enumerate(lines):
        if line[:7] != 'Вопрос' :
         lines[i] = line.replace('Вопрос ','')
      
      for item in lines[:-1]:
        item = item.split('\nОтвет')
        
        if(len(item)<2):
          continue
        
        question_to_strip = item[0] 
        answer_to_strip = item[1]
        question_line_to_strip = question_to_strip.find('\n')+1
        answer_line_to_strip_first = answer_to_strip.find('\n')
        answer_line_to_strip_second = answer_to_strip.find('\n\n')
        
        question =   question_to_strip[question_line_to_strip:].strip()
        answer = answer_to_strip[answer_line_to_strip_first:answer_line_to_strip_second].strip()
        questions.append((question, answer))
           
       
  return questions

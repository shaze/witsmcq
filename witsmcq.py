#!/usr/bin/env python3
# (c) Scott Hazelhurst, University of the Witwatersrand, Johannesburh, 2023

import sys

import reportlab
from reportlab.pdfgen import canvas
import pandas as pd
import argparse

def getArgs():
   parser = argparse.ArgumentParser(description='Fedback for  MCQ')
   parser.add_argument('responses', help='response dat file',type=str)
   parser.add_argument('answers', help='answer excel',type=str)   
   parser.add_argument('--heading ',dest="heading",type=str,default="Test Feedback")   
   parser.add_argument('--output-name ',dest="oname",type=str,default="results")
   parser.add_argument('--num-rows', dest='num_rows',type=int, default=25)
   
   args = parser.parse_args()
   return args

choice = {'X....':'a','.X...':'b', '..X..':'c', '...X.':'d', '....X': 'e', '.....':'-'}


      


args = getArgs()



def result(correct,resp):
    return (1,"\u2713") if correct.upper()==resp.upper() else (0,"\u2717")

def get_results(line,num_questions):
      student = line[40:47]
      answers = line[48:].strip()
      resp = ""
      for chunk in [answers[i:i+5] for i in range(0, 5*num_questions, 5)]:
         resp=resp+choice.get(chunk,"X")
      return (student, resp)

 
def showResult(c, rf,correct):
    all_results=[]
    all_responses=[]
    odd_numbers = []
    for r in rf:
        if len(r)==1: continue
        (student, this_answer) = get_results(r.strip(),len(correct))
        if " " in student or len(student)<6: odd_numbers.append(student)
        all_responses.append((student,this_answer))
    all_responses.sort()
    if len(odd_numbers)>0:
       print("""
          The following student numbers seem odd -- < > used as quote symbols
          so that spaces and/or empty strings can be clearly seen
       """)
       for num in odd_numbers:
          print("<%s>"%num)
    for student, this_answer in all_responses:
        c.setFont('Helvetica-Bold', 14)
        c.drawString(10,800,"%s : %s "%(args.heading,student))
        c.setFont('Helvetica', 11)                
        x=-15
        num_correct=0
        for q, student_answer in enumerate(this_answer):
            if q%args.num_rows == 0:
                x=x+50
                y=780
            (mark, symbol)= result(correct[q+1],student_answer)
            num_correct=num_correct+mark
            c.drawString(x,y,"%3d.  %s "%(q+1,symbol))
            y=y-20
        c.drawString(10,20,"%d/%d = %4.1f%%"%(num_correct,len(correct),\
                                              100*num_correct/len(correct)))
        all_results.append((student,num_correct,"%4.1f"%(100*num_correct/len(correct))))
        c.showPage()
    return all_results

    
c = canvas.Canvas(args.oname+".pdf")


correct_df  = pd.read_excel(args.answers)
correct = dict(zip(correct_df['Question Number'],correct_df['Answer']))




rf = open(args.responses)
all_results=list(zip(*showResult(c,rf, correct)))
all_map = { 'Student Number':all_results[0], 'Mark':all_results[1], \
                  'Percentage':all_results[2] }
df = pd.DataFrame(all_map)
df.to_excel(args.oname+".xlsx",index=False)
c.save()

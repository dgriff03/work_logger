from datetime import datetime
import pymysql
import sys


conn = pymysql.connect(host='localhost', db='work', user='root')
conn.autocommit(True)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS logger(
        id MEDIUMINT NOT NULL AUTO_INCREMENT,
        name varchar(64) not null,
        start_time datetime,
        end_time datetime,
        PRIMARY KEY (id)
    )
	""")


if len(sys.argv) != 3:
	print "Useage: python work.py [work|display] [task_name]"
	exit(1)

ty = sys.argv[1].lower()
task_name = sys.argv[2]
if ty == "work":
	start_time = datetime.now()

	try:
		end_signal = input('Hit enter to end task: ')
	except:
		pass
	end_time = datetime.now()

	cur.execute("""INSERT into logger (name,start_time,end_time) values (%s,%s,%s) """, 
		(task_name,start_time,end_time,))

elif ty == "display":
	cur.execute("""SELECT name,SUM(TIMESTAMPDIFF(SECOND,start_time,end_time))
	 from logger 
	 where name=%s
	 group by name
	 order by SUM(TIMESTAMPDIFF(SECOND,start_time,end_time)) desc
	 ;""",(task_name,))
	info = cur.fetchone()
	if info:
		print "{}: {} seconds".format(info[0],info[1])
else:
	print "Useage: python work.py [work|display] [task_name]" 


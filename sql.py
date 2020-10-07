import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('db.sqlite3')



tables = ['catalog_author', 'catalog_bookInstance', 'catalog_book', 'catalog_genre', 'catalog_language', 'catalog_myUser']

data = [
	(1, 'JavaScript & jQuery Programming', 'This book explains how JavaScript can be used in browsers to make websites more interactive, interesting, and user-friendly. You will also learn about jQuery because it make JavaScript a lot easier.', '9781118531648', 1),
	(2, 'Angular Up & Running', 'What makes Angular a great technology and framework is the community around it - those who contribute to the core framework, or develop plug-ins for it, as well as those who use it on a day-to-day basis.', '9781491999837', 2),
	(3, 'Mastering Photoshop For Web Designers', 'This eBook contains 11 articles that cover useful techniques and tricks from experts such as retouching, cloning, compositing, obscure Photoshop time-savers and designing for iPhone. You may know some of them, but hopefully not all of them.', '9783943075120', 3),
	(4, 'Black Hat Python Programming', 'This book covers a large range of topics that an enterprising young hacker would need to get off the ground. It includes walk-throughs of how to read and write network packets, how to sniff the network, as well as anything you might need for web application auditing and attacking', '9781593275907', 4),
	(5, 'The Name of the Wind', 'Told in Kvothes own voice, this is the tale of the magically gifted young man who grows to be the most notorious wizard his world has ever seen.', '9781473211896', 5),
	(6, 'In Search of Lost Time', 'Swanns Way, the first part of A la recherche de temps perdu, Marcel Prousts seven-part cycle, was published in 1913. In it, Proust introduces the themes that run through the entire work.', '9782070754922', 6),
	(7, 'Bash Cookbook', 'This book covers bash, the GNU Bourne Again Shell, which is a member of the Bourne family of shells that includes the original Bourne shell sh, the Korn shell ksh, and the Public Domain Krn Shell pdksh. While these and other shells such as dash, and zsh are not specifically covered, odds are that most of the scripts will work pretty well with them.', '9780596526788', 7),
	(8, 'Introduction to Programming Using Java', 'INTRODUCTION TO PROGRAMMING USING JAVA is a free introductory computer programming textbook that uses Java as the language of instruction. It is suitable for use in an introductory programming course and for people who are trying to learn programming on their own.There are not prerequisites beyond a general familiarity with computers and programs.', '1111111111111', 10),
	(9, 'Learning Python', 'This book provides an introduction to the Python programming language. Python is a popular open source programming language used for both standalone programs, and remarkably easy and fun to use.', '9780596158064', 11),
	(10, 'Beginning Android Programming with Android Studio', 'This book is targeted for the beginning Android Developer who wants to start developing applications using Googles Android SDK. To truly benefit from this book, you should have some programming background and at least be familiar with object-oriented programming (OOP) concepts.', '9781118705599', 12),
	(11, 'Beginning iOS Programming for Dummies', 'This book guides you through the iOS SDK and how to build high-quality applications using it. It focuses on iOS y and Xcode version 5 and is of significant value to software developers, regardless of their level of experience.', '9781118799277', 13),
	(12, 'Android 3 SDK Programming For Dummies', 'This book guides you through the Android SDK and how to build high-quality applications using it. It focuses on Android and Android Studio version 5 and is of significant value to software developers, regardless of their level of experience.', '9781118799271', 13)
]

# data = [
# 	('071ae45733d54993b6ca325b4e89c6e5', 'Manufactured in the United States of America', eval('None'), 'm', 1),
# 	('871ac1e367b24292af8cd1c45a8815ae', 'Printed in the United States of America', datetime(2020,8,28).strftime("%Y-%m-%d"), 'o', 2),
# 	('6a39cc5eee874d2cb5e9a80458c59f58', 'Printed by Smashing Media in Germany', eval('None'), 'a', 3),
# 	('a338183c736e45df9dca9a4a8f2fb97b', 'Printed in the United States of America', eval('None'), 'r', 4),
# 	('7e9197d5cdb44a9f99550206ba5c75cf', 'Printed in the United States of America', eval('None'), 'a', 5),
# 	('9808820455cd46aab3bbb8db216b2cc9', 'Printed in France', eval('None'), 'm', 6),
# 	('696ad693e79a489981819c467a4bd5ab', 'Printed in the United States of America', eval('None'), 'a', 6),
# 	('a0cf1ca4eaac4511b668a95ed0e2e5fb', 'Manufactured in the United States of America', datetime(2020,9,19).strftime("%Y-%m-%d"), 'o', 1),
# 	('7178671d9dad499c99519a9d2d79f91b', 'Published by OReilly Media, Inc., 1005 Gravenstein Highway North, Sebastopol, CA 95472', datetime(2020,10,15).strftime("%Y-%m-%d"), 'o', 7),
# 	('462cae31d0b84b3fab951ddccb5a12ce', 'Printed in United States of America', eval('None'), 'a', 8),
# 	('f766226d0541454da96d6e6720ccdb1c', 'Printed in the United States of America.', eval('None'), 'a', 9),
# 	('80fb7d9e69a14952b7afafbd4b1954aa', 'Printed in the United States of America', datetime(2020,10,16).strftime("%Y-%m-%d"), 'm', 9),
# 	('0da143f307f24b4c99d678688d0ff65b', 'Printed in the United States of America', eval('None'), 'a', 9),
# 	('947f3f2ab64e497793c69a11f92eabb7', 'Printed in the United States of America', datetime(2021,4,15).strftime("%Y-%m-%d"), 'o', 9),
# 	('8851c457dab94592b7f34c29c24827ad', 'Printed in the United States of America', datetime(2020,9,25).strftime("%Y-%m-%d"), 'r', 9),
# 	('ac01959e0a98464fba582014db1b933f', 'Printed in the United States of America', eval('None'), 'a', 9),
# 	('0d1d387d4e274ed2ade22b6ff742f300', 'Printed by Smashing Media in Germany', datetime(2020,9,8).strftime("%Y-%m-%d"), 'm', 3),
# 	('78e05db671494ddb8247a6cde672d7e2', 'Printed in the United States of America', eval('None'), 'a', 4),
# 	('bb21023d0624478cbb6f9c10deff325a', 'Printed in the United States of America', eval('None'), 'a', 4),
# 	('3bc12ea0c2a4440ba1a10906982ea062', 'Printed in the United States of America', eval('None'), 'a', 4),
# 	('58b55391e64a42d49af0047298c4a47a', 'Published by OReilly Media, Inc., 1005 Gravenstein Highway North, Sebastopol, CA 95472', eval('None'), 'a', 7),
# 	('7e52a272892145049745d03e3c6be076', 'Published by OReilly Media, Inc., 1005 Gravenstein Highway North, Sebastopol, CA 95472', eval('None'), 'a', 7),
# 	('7bd47aea8ef74e139425e092fbdfc621', 'Manufactured in the United States of America', eval('None'), 'a', 1),
# 	('22c8b053be914ac896f7ad27b7c13714', 'Manufactured in the United States of America', eval('None'), 'a', 1),
# 	('8208e4e12f7343caa26b865d02fe58fb', 'Manufactured in the United States of America', eval('None'), 'a', 10),
# 	('1cc7a4e596be4b78b0889b8113ccf986', 'Published by: John Wiley & Sons, Inc., 111 River Street, Hoboken, NJ 07030-5774, www.wiley.com', eval('None'), 'a', 11),
# 	('1bc16faab4ba45aa8205046cb1764b65', 'Published by: John Wiley & Sons, Inc., 111 River Street, Hoboken, NJ 07030-5774, www.wiley.com', eval('None'), 'a', 12)
# ]

c = conn.cursor()

# c.execute("DELETE FROM catalog_bookInstance")
c.executemany("INSERT INTO catalog_book VALUES (?,?,?,?,?)", data)
# rows = ''
# for table in tables:
# 	data = json.loads(open('%s.json'%table).read())
# 	for data_item in data:
# 		print(data_item)
# 		c.execute("INSERT INTO %s VALUES %s" %(table, data_item))
# 		print("INSERT INTO %s VALUES %s"%(table, data_item))

conn.commit()

# for i in c.execute("PRAGMA table_info(catalog_bookInstance)"):
# 	print(i)

conn.close()


	# for row in c.execute('SELECT * FROM %s'%table):
	# 	print(row)



	# jsong_string = ''
	# rows = ''
	# for row in c.execute('SELECT * FROM %s' %table):
	# 	rows += '\t"%s",\n'%str(row)
	# json_string = '[\n%s\n]'%rows[0:-2]
	# with open('%s.json'%table, 'w') as json:
	# 	json.write(str(json_string))
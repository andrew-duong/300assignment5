import mysql.connector
from mysql.connector import errorcode
 
#username = input("Please enter your username: ")

passw = input('\nPlease enter your password: ')

try:
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",  # should be username
        password= passw,  # should be password
        database="olympicarchery")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    exit()

class table:
    def __init__(self, table_name, num_columns, column_list):
        self.table_name = table_name  # string
        self.num_columns = num_columns  # int
        # list of columns[[column name, column type(either varchar), char or int, can be null?, length of field(if applicable)]]
        self.column_list = column_list

def print_tables():
    '''Will look at the list table_list and print out what the valid selections are, and return what the selection is.
    Will also check to see if input is valid or not'''

    for i, table in enumerate(table_list):
        print('Press [{}] for {}'.format(i, table.table_name))
    while True:
        try:
            selection = int(input("\nPlease enter your choice: "))
            if selection >= 0 and selection <= len(table_list) - 1:
                return selection
        except ValueError:
            pass
        print('Invalid Input, Please try again')

def check_constraints(constraints):
    '''Function returns a user input value that will be used in a tuple'''
    # constraints is a nested list within columns list, 0 = column name, 1 = type of variable, 2 = is 'not null' specified, 3 = length of varchar if applicable
    # part 1, print out what the constraints are to the user
    while True:
        print('\nInput the value for {} which is '.format(
            constraints[0]), end='')
        if constraints[1] == 'integer':
            if constraints[2] == 0:
                print('an integer that can be Null:')
            else:
                print('an integer that cannot be Null:')
            user_input = input()
            try:
                int(user_input)
                return user_input
            except ValueError:
                if user_input.lower() == 'null' and constraints[2] == 0:
                    return user_input
                print('\nInvalid Input')
        elif constraints[1] == 'varchar' or constraints[1] == 'char':
            if constraints[2] == 0:
                print('a string that can be Null ', end='')
            else:
                print('a string that cannot be Null ', end='')
            print('that is no more than {} character(s) long:'.format(
                constraints[3]))
            user_input = input()
            if user_input.lower() == 'null' and constraints[2] == 0:
                return user_input
            elif len(user_input) <= constraints[3] and user_input.lower() != 'null':
                return user_input
            print('\nInvalid Input')

        else:
            print('error in reading in the constraint type')
            return

def insert():
    '''Function will insert 1 tuple at a time into a table as specified by the user.
       Error Handling is also built in in case key constraints are violated'''

    cur = cnx.cursor(buffered=True)
    print("Please select the table you would like to insert into.")
    selection = print_tables()
    print("You have chosen to insert into {}\nThere are {} columns".format(
        table_list[selection].table_name, table_list[selection].num_columns))
    insert_list = [] #list that will store the tuple to be inserted into the chosen table

    for i in range(table_list[selection].num_columns): 
        insert_list.append(check_constraints(table_list[selection].column_list[i])) # Creates insert_list with the help of check_constraints()
        
    statement = 'insert into ' + table_list[selection].table_name + '('
    
    for i, value in enumerate(table_list[selection].column_list): #statement after this for loop will be of form 'Insert into table(column 1, column2...etc)
        statement += value[0]
        if i != len(table_list[selection].column_list)-1:
            statement += ','


    statement += ') values ('

    for i, value in enumerate(insert_list): #after for loop statement will be 'insert into table(col 1, col 2... etc)values(attribute 1, attribute 2...etc)
        # adding each element
        if insert_list[i].lower() == 'null': #null values don't have '' around them, hence the need to check
            statement += value
        else:
            statement += '\'' + value + '\''
        if i != len(insert_list)-1:
            statement += ','
            
    statement += ');'

    try: #executing statement
        cur.execute(statement) 
        cnx.commit()
    except: #error handling
        print('An error occured when trying to execute \'{}\'.\nPlease Check that Any Foreign Keys Match the Primary Keys they reference'.format(statement))
    print("The table {} is displayed.\n".format(table_list[selection].table_name))
    cur.execute("select * from {}".format(table_list[selection].table_name))
    rows = cur.fetchall()
    for i in table_list[selection].column_list:
      print("{:<15}".format(i[0]), end='')
    print()
    for i in range(len(rows)):
      for j in rows[i]:
        if j == None:
            j = 'NULL'
        print("{:<15}".format(j), end='')
      print()
    cur.close()
    return

def delete():
    cur = cnx.cursor(buffered=True)
    print("\nPlease select the table you would like to delete from.")
    selection = print_tables()
    print("\nYou have chosen to delete from {}.".format(
        table_list[selection].table_name))
    statement = 'delete from ' + table_list[selection].table_name
    show = "select * from " + table_list[selection].table_name
    print("\nPress [1] to delete all tuples in your selected table.\nPress [2] to delete a record.")
    while True:
      try:
        useropt = int(input("\nPlease enter your choice: "))
        if 0 < useropt < 3:
          break
      except:
          print('Invalid Input, Please try again')
    if useropt == 1:
      print("You have chosen to delete all tuples in {}".format(table_list[selection].table_name))
      try:
        cur.execute(statement)
        cnx.commit()
      except:
        print("The table, {}, is unable to be modified due to foreign key constraints.".format(table_list[selection].table_name))
    elif useropt == 2:
      print("\nPlease select the column you would like to delete from.")
      choice_dict = {}
      choice_key =[]
      for i, v in enumerate(table_list[selection].column_list):
        print("Press [{}] for {}".format(i, table_list[selection].column_list[i][0]))
        choice_dict[v[0]] = i
        choice_key.append(v[0])
      while True:
        try:
          useroptcol = int(input("\nPlease enter your choice: "))
          if int(choice_dict.get(choice_key[0])) <= useroptcol <= int(choice_dict.get(choice_key[-1])):
            break
        except ValueError:
            print('Invalid Input, please try again.')
        except:
            print("Invalid Input, please try again.")
      statement += " where " + choice_key[useroptcol] + "="
      show = "select " + choice_key[useroptcol] + " from " + table_list[selection].table_name
      cur.execute(show)
      rows = cur.fetchall()
      print("\n{}".format(choice_key[useroptcol]))
      for i in range(len(rows)):
        print(rows[i][0])
      try:
        whereclause = str(input("Please type in any entry from the table above to remove (if multiple entries have the same value, they will all be removed.): "))
        statement += "\"{}\";".format(whereclause)
        cur.execute(statement, multi=True)
        cnx.commit()
      except:
        print('The selected table/entry cannot be removed due to foreign key constraints.')
    print("The table {} is displayed.\n".format(table_list[selection].table_name))
    cur.execute("select * from {}".format(table_list[selection].table_name))
    rows = cur.fetchall()
    for i in table_list[selection].column_list:
      print("{:<15}".format(i[0]), end='')
    print()
    for i in range(len(rows)):
      for j in rows[i]:
        if j == None:
            j = 'NULL'
        print("{:<15}".format(j), end='')
      print()
    cur.close()
    return

def update():
  cur = cnx.cursor(buffered=True)
  print("Please select the table you would like to update.")
  selection = print_tables()
  print("You have chosen to update from the table", table_list[selection].table_name)
  statement = "UPDATE " + table_list[selection].table_name
  while(True):
    index_set = -1
    for i in range(0,len(table_list[selection].column_list)):
      print(table_list[selection].column_list[i][0])
    set_loc = input("Please select on of the above options where you would like to update: ")
    for j in range(0,len(table_list[selection].column_list)):
      if set_loc == table_list[selection].column_list[j][0]:      
        statement += "\nSET " + table_list[selection].column_list[j][0] + "="
        index_set = j
        break
    if index_set != -1:
      break
    else: print("Please enter a valid response.")

  if "integer" == table_list[selection].column_list[index_set][1]:
    while(True):
      set_clause = input("Please enter the updated value: ")
      if set_clause.upper() == 'NULL' and table_list[selection].column_list[index_set][2] == 1:
        print("NULL value not allowed.")
      elif set_clause.isdigit() == True:
        break
      else:
        print("Error please enter a valid integer value.")
    statement += set_clause

  else:
    while(True):
      while(True):
        set_clause = input("Please enter the updated value: ")
        if set_clause.upper() == 'NULL' and table_list[selection].column_list[index_set][2] == 1:
          print("NULL value not allowed.")
        else:
          break
      if len(set_clause) <= table_list[selection].column_list[index_set][3]:
        break
      else: print("Please input a number less than or equal to", table_list[selection].column_list[index_set][3])
    statement += "'"+set_clause+"'"

  while(True):
    index_where = -1
    for i in range(0,len(table_list[selection].column_list)):
      print(table_list[selection].column_list[i][0])
    where_loc = input("Please select on of the above options for the location of the WHERE clause: ")
    for n in range(0,len(table_list[selection].column_list)):
      if where_loc == table_list[selection].column_list[n][0]:
        statement += "\nWHERE " + table_list[selection].column_list[n][0] + "="
        index_where = n
        break
    if index_where != -1:
      break
    else: print("Please enter a valid response.")

  if "integer" == table_list[selection].column_list[index_where][1]:
    while(True):
        where_clause = input("Please enter the value for the WHERE clause: ")
        if where_clause.upper() == 'NULL' and table_list[selection].column_list[index_set][2] == 1:
          print("NULL value not allowed.")
        elif where_clause.isdigit() == True:
          break
        else:
          print("Error please enter a valid integer value.")
    statement += where_clause

  else:
    while(True):
      while(True):
        where_clause = input("Please enter the value for the WHERE clause: ")
        if where_clause.upper() == 'NULL' and table_list[selection].column_list[index_set][2] == 1:
          print("NULL value not allowed.")
        else:
          break
      if len(where_clause) <= table_list[selection].column_list[index_where][3]:
        break
      else: print("Please input a number less than or equal to", table_list[selection].column_list[index_where][3])
    statement += "'"+where_clause+"'"

  try:
    cur.execute(statement)
    cnx.commit()
    for i in table_list[selection].column_list:
      print("{:<15}".format(i[0]), end=' ')
    print()
    cur.execute("SELECT * FROM {}".format(table_list[selection].table_name))
    rows = cur.fetchall()
    for i in range(len(rows)):
      for j in rows[i]:
        print("{:<15}".format(j), end=' ')
      print()

  except:
    print('An error occured when trying to execute \'{}\'.\nPlease Check that Any Foreign Keys Match the Primary Keys they reference'.format(statement))
    cur.execute('select * from{}'.format(table_list[selection].table_name))
    cur.fetchall()
  cur.close()

def valid_sql_object_name():
    #helper function that is used to check if a user input object name (table name, column name, view name... etc) is valid or if it will cause errors
    while 1:
        name = input()
        if '_' == name[0] or name[0].isnumeric() == True:
            print('\nObject Name cannot start with underscores or numbers.')
            continue
        for i in range(1, len(name)):
            if name[i].isalnum() == False and name[i] != '_':
                print(
                    '\nObject Name Can only contain alphanumeric characters and underscores.')
                break
            elif i == len(name)-1:
                return name

def isnull():
    #helper function for create(), returns a 0 or 1, depending if null values are allowed in the column
 while 1:
  isnull = input('Press [0] if \'Null\' is allowed in this column\nPress [1] if \'Null\' is not allowed in this column:\n')
  if isnull in ['0','1']:
    return isnull
  else:
    print('Invalid Input')

def get_length():
    #helper function for create(), returns the length of the character field as determined from the user
  while 1:
    length = input('Input the Length of the character field: ')
    if length.isnumeric() == True:
      return int(length)
    else:
      print('Invalid Input, Please input an Integer.')

def view():
  cur = cnx.cursor(buffered = True)

  print('\nWhat would you like to name the VIEW?:', end = ' ')
  view_name = valid_sql_object_name()

  statement = "CREATE VIEW " + view_name + " AS"
  print("\nQuery statement: {}".format(statement))
 
  print("\nPress [0] for Athlete.\nPress [1] for Coach.\nPress [2] for Country.\nPress [3] for Event Schedule.\nPress [4] for Individual Results.\nPress [5] for Participant.\nPress [6] for Team.\nPress [7] for Team Results.")
 
  while True:
      try:
        selection = int(input("\nPlease select a table to query FROM: "))  
        if selection >= 0 and selection <= len(table_list) - 1:
          break
      except ValueError:
        print('Invalid Input, Please try again')
 
  print("\n")
 
  for i in range(0,len(table_list[selection].column_list)):
    print('Press [{}] for {}'.format(i, table_list[selection].column_list[i][0]))
 
  n = len(table_list[selection].column_list)
  print("\nThere are {} columns.".format(n))
 
  while True:
      try:
        num_select = int(input("\nHow many columns would you like to SELECT: "))
        if selection >= 0 and selection <= len(table_list) - 1:
          break
      except ValueError:
        print('Invalid Input, Please try again')
 
  statement += " SELECT"
 
  print("\n")

  wrist = []
 
  while(num_select > 0):
    while True:
      try:
        selection2 = int(input("Please select which columns to SELECT FROM: "))
        wrist.append(selection2)
        if selection >= 0 and selection <= len(table_list) - 1:
          break
      except ValueError:
        print('Invalid Input, Please try again\n')
    statement += " " + table_list[selection].column_list[selection2][0]
    if num_select != 1:
      statement += ','
    num_select -= 1
 
  statement += " " + "FROM" + " " + table_list[selection].table_name
  print("\nQuery statement: {}".format(statement))
 
  print("\nPress [0] for No")
  print("Press [1] for Yes")
 
  while True:
      try:
        ask_where = int(input("\nWould you like to add more to the query?: "))  
        if ask_where >= 0 and ask_where <= 1:
          break
      except ValueError:
        print('Invalid Input, Please try again')
 
  if ask_where == 1:
    statement += " " + input("\nTo execute additional clauses please type the clause as you would in SQL: ")
 
  print("\nQuery statement: {}\n".format(statement))
  
  while(True):
    try:
      cur.execute(statement)
      cnx.commit()
      break
    except:
      print('An error occured when trying to execute \'{}\'.\nPlease Check that Any Foreign Keys Match the Primary Keys they reference'.format(statement))
      cur.execute('select * from{}'.format(table_list[selection].table_name))
      cur.fetchall()
 
  statement1 = "SELECT * FROM " + view_name
  cur.execute(statement1)
  
  rows = cur.fetchall()

  print('{:^}'.format(view_name))
  print()
 
  for i in wrist:
    print('{:<15}'.format(table_list[selection].column_list[i][0]), end = '')
  print()
  
  for i in range(len(rows)):
    for j in rows[i]:
      print('{:<15}'.format(j), end = '')
    print()
  
  cur.close()
 
def query():
  cur = cnx.cursor(buffered = True)
 
  print("\nPress [0] for Athlete.\nPress [1] for Coach.\nPress [2] for Country.\nPress [3] for Event Schedule.\nPress [4] for Individual Results.\nPress [5] for Participant.\nPress [6] for Team.\nPress [7] for Team Results.")
 
  while True:
      try:
        selection = int(input("\nPlease select a table to query FROM: "))  
        if selection >= 0 and selection <= len(table_list) - 1:
          break
      except ValueError:
        print('Invalid Input, Please try again')
 
  print("\n")
 
  for i in range(0,len(table_list[selection].column_list)):
    print('Press [{}] for {}'.format(i, table_list[selection].column_list[i][0]))
 
  n = len(table_list[selection].column_list)
  print("\nThere are {} columns.".format(n))
 
  while True:
      try:
        num_select = int(input("\nHow many columns would you like to SELECT: "))
        if selection >= 0 and selection <= len(table_list) - 1:
          break
      except ValueError:
        print('Invalid Input, Please try again')
 
  statement = "SELECT"
 
  print("\n")

  wrist = []
 
  while(num_select > 0):
    while True:
      try:
        selection2 = int(input("Please select which columns to SELECT FROM: "))
        wrist.append(selection2)
        if selection >= 0 and selection <= len(table_list) - 1:
          break
      except ValueError:
        print('Invalid Input, Please try again\n')
    statement += " " + table_list[selection].column_list[selection2][0]
    if num_select != 1:
      statement += ','
    num_select -= 1
 
  statement += " " + "FROM" + " " + table_list[selection].table_name
  print("\nQuery statement: {}".format(statement))

  print("\nPress [0] for No")
  print("Press [1] for Yes")
 
  while True:
      try:
        ask_where = int(input("\nWould you like to add more to the query?: "))  
        if ask_where >= 0 and ask_where <= 1:
          break
      except ValueError:
        print('Invalid Input, Please try again')
 
  if ask_where == 1:
    statement += " " + input("\nTo execute additional clauses please type the clause as you would in SQL: ")
 
  print("\nQuery statement: {}\n".format(statement))
 
  try:
    cur.execute(statement)
    cnx.commit()
  except:
    print('An error occured when trying to execute \'{}\'.\nPlease Check that Any Foreign Keys Match the Primary Keys they reference'.format(statement))
    cur.execute('select * from{}'.format(table_list[selection].table_name))
    cur.fetchall()
 
  rows = cur.fetchall()

  for i in wrist:
    print('{:<15}'.format(table_list[selection].column_list[i][0]), end = '')
  print()
  
  for i in range(len(rows)):
    for j in rows[i]:
      print('{:<15}'.format(j), end = '')
    print()

  cur.close()
   
def create():
    #function creates a new table along with all the column constraints, primary keys and foreign keys, creates a new instance in class table() as well
    cur = cnx.cursor(buffered=True)
    print('Enter the Name for the Table:')
    table_name = valid_sql_object_name()
    while 1: #getting the number of columns
        try:
            number_columns = int(input('Enter the Number of Columns this Table will have: '))
            if number_columns > 0:
                break
        except ValueError:
            pass
        print('Invalid Input, Please try again')
  
    column_list = list(range(number_columns))  #column list will have the exact format that is used in class table.column_list

    statement = 'Create table ' + table_name + '('
    
    for i in range(number_columns): #for loop iterates for each column, and defines the variable type and constraints for each column
        column_list[i] = list(range(4))
        print('Enter the Name for Column {}:'.format(i))
        column_list[i][0] = valid_sql_object_name()
        statement += column_list[i][0] + ' '
        while 1:
            print('Press [1] if this Column is for an Integer\nPress [2] if this Column is for a Variable Character Field (Varchar)\nPress [3] if this Column is for a Character Field (Char)')
            variable_type = input()
            if variable_type == '1':
                column_list[i][1] = 'integer'
                statement += 'integer'
                break
            elif variable_type == '2':
                column_list[i][1] = 'varchar'
                column_list[i][3] = get_length()
                statement += 'varchar({})'.format(column_list[i][3])
                break
            elif variable_type == '3':
                column_list[i][1] = 'char'
                column_list[i][3] = get_length()
                statement += 'char({})'.format(column_list[i][3])
                break
            else:
                print('Invalid Input')

        column_list[i][2] = int(isnull())
        if column_list[i][2] == 1:
            statement += ' not null'
        if i != number_columns - 1:
            statement += ','
    #statement will now have the form 'Create Table table(Column 1 Integer not null, column 2 varchar(25),... etc, )
    while 1: #defining which column is the primary key
        try:
            primary_key = int(input('Enter which column number is the primary key(starting at 0):\n'))
            if primary_key <= number_columns-1 and primary_key >= 0:
                statement += ', primary key (' + column_list[primary_key-1][0]
                again = input('Press [1] if you would like to input another primary key,\nPress any other key to continue: ')
                if again == '1':
                  statement += ','
                break
            continue
        except ValueError:
            pass
        print('Invalid Input')
        again = input('Press [1] if you would like to input another primary key,\nPress any other key to continue:\n')
        if again == '1':
            statement += ','
            continue

    statement += ')'
    
    while 1:#defining which column(s) are foreign keys and what they reference
        foreign = input('Press [1] if you would like to input a(nother) foreign key,\nPress any other key to continue:\n')
        if foreign == '1':
            
            try:
                foreign_key = int(input('Enter which column number is the foreign key(starting at 0): '))
                if foreign_key <= number_columns-1 and foreign_key >= 0:
                    statement += ', foreign key(' + column_list[foreign_key-1][0]
                    print('Now select the table that the foreign key references')
                    reference_table = print_tables()
                    print('\nNow select which column the foreign key references\n')
                    for i in range(table_list[reference_table].num_columns):
                        print('Select [{}] for {}'.format(i, table_list[reference_table].column_list[i][0]))
                    while 1:
                        try: 
                            reference_attribute = int(input('\nPlease enter your choice: '))
                            if reference_attribute <= table_list[reference_table].num_columns - 1 and reference_attribute >= 0:
                                statement += ') references ' + table_list[reference_table].table_name + '(' + table_list[reference_table].column_list[reference_attribute][0] + ')'
                                break
                        except ValueError:
                            print('Invalid Input')
            except ValueError:
                print('Invalid Input')

        else: 
            break
            
    statement += ');'#statement is complete

    try:#executing statement
        cur.execute(statement)
        cnx.commit()
        table_list.append(table(table_name, number_columns, column_list))
    except: #error handling
        print('\nAn error occured when trying to execute \'{}\'.\nPlease check that primary keys and foreign keys reference other tables correctly'.format(statement))
    print("The table {} is displayed.\n".format(table_name)) #printing the table
    cur.execute("select * from {}".format(table_name))
    rows = cur.fetchall()
    for i in column_list:
      print("{:<15}".format(i[0]), end='')
    print()
    cur.close()
    return

def alter():
  cur = cnx.cursor(buffered=True)
  print("Please select the table you would like to alter.")
  selection = print_tables()
  print("You have chosen to alter from the table", table_list[selection].table_name)
  while(True):
    statement = "ALTER TABLE " + table_list[selection].table_name
    print("\nPress [1] to ADD a column.\nPress [2] to DROP a column.\nPress [3] to rename a column.\nPress [4] to rename the table.\nPress [5] to quit the alter menu")
    option = input("Please enter your option: ")

    if option == '1':
        while(True):
          check = 0
          name = input("Please enter the name of the column you would like to ADD: ")
          for i in range(0,len(table_list[selection].column_list)):
            if name.upper() == table_list[selection].column_list[i][0].upper():
              print("Error column name already exists.")
              check = 0
              break
            check = 1
          if check == 1:
            break
        statement += "\nADD " + name

        while(True):
          print("Types of constraints include: varchar, char, integer")
          constraint = input("Please specify the type of constraint: ")
          if constraint == "varchar" or "char" or "integer":
            statement += " " + constraint.upper() + " "
            break
          else: print("Please enter a valid response.")
        if constraint != "integer":
          while(True):
            numchar = input("Please enter a limit (whole number greater than 0):")
            if int(numchar) != 0:
              statement += "(" + numchar +") "
              break
            else: print("Please enter a valid response.")
        while(True):
          nullinput = input("Please type in 0 for NULL values allowed or 1 for NULL values not allowed: ")
          if nullinput == '1':
            statement += "NOT NULL"
            break
          elif nullinput == '0':
            statement += "NULL"
            break
          else: print("Please enter a valid response.")
        if constraint == "integer":
          table_list[selection].column_list.append([name,constraint,int(nullinput)])
        else:
          table_list[selection].column_list.append([name,constraint,int(nullinput),int(numchar)])
        cur.execute(statement)
        cnx.commit()
        select_statement = "DESCRIBE "+ table_list[selection].table_name
        cur.execute(select_statement)
        rows = cur.fetchall()
        print("The names of all the columns are listed below: ")
        for j in rows:
          print(j[0])
        cur.close()
        
    elif option == '2':
      for i in range(0,len(table_list[selection].column_list)):
        print(table_list[selection].column_list[i][0])
      while(True):
        index = -1
        original = input("Please enter the name of one of the above columns you would like to DROP: ")
        for j in range(0,len(table_list[selection].column_list)):
          if original == table_list[selection].column_list[j][0]:
            statement += " DROP COLUMN " + table_list[selection].column_list[j][0]
            index = j
            del table_list[selection].column_list[j] 
            break
        if index != -1:
          break
        else: print("Please provide a valid input.")
      cur.execute(statement)
      cnx.commit()
      select_statement = "DESCRIBE "+ table_list[selection].table_name
      cur.execute(select_statement)
      rows = cur.fetchall()
      print("The names of all the columns are listed below: ")
      for j in rows:
          print(j[0])
      cur.close()

    elif option == '3':
      for i in range(0,len(table_list[selection].column_list)):
        print(table_list[selection].column_list[i][0])
      index = -1
      while(True):
        original = input("Please enter the name of one of the above columns you would like to modify: ")
        for j in range(0,len(table_list[selection].column_list)):
          if original == table_list[selection].column_list[j][0]:
            statement += " RENAME COLUMN " + table_list[selection].column_list[j][0]
            index = j
            break
        if index != -1:
          break
        else: print("Please provide a valid input.")
      rename = input("Please enter the desired name: ")
      table_list[selection].column_list[index][0] = rename
      statement += " TO " + rename
      cur.execute(statement)
      cnx.commit()
      select_statement = "DESCRIBE "+ table_list[selection].table_name
      cur.execute(select_statement)
      rows = cur.fetchall()
      print("The names of all the columns are listed below: ")
      for j in rows:
          print(j[0])
      cur.close()

    elif option == '4':
        rename = input("Please enter the desired name: ")
        table_list[selection].table_name = rename
        statement += " RENAME TO " + rename
        cur.execute(statement)
        cnx.commit()
        print("The names of all the tables are listed below: ")
        select_statement = "SHOW tables"
        cur.execute(select_statement)
        rows = cur.fetchall()
        for j in rows:
          print(j, end="\t")
        cur.close()

    elif option == '5':
        break
    else: print("Invalid input try again")

def choicemenu():
  while (True):
    print("\nPress [1] to insert data.\nPress [2] to delete data.\nPress [3] to update data.\nPress [4] to create a table.\nPress [5] to create a view.\nPress [6] to alter data.\nPress [7] to create a query.\nPress [0] to quit the program.\n")
    option = input("Please enter your option: ")
    if option == '1':
        insert()
    elif option == '2':
        delete()
    elif option == '3':
        update()
    elif option == '4':
        create()
    elif option == '5':
        view()
    elif option == '6':
        alter()
    elif option == '7':
        query()
    elif option == '0':
        break
    else:
        print("Invalid Input")
  return print("Quitting program...")

def build_table_class():
    #This function initializes what the starting form of the 'Olympic Archery' Database should look like
  athlete = table('athlete', 4, [['OlympicID', 'varchar', 1, 10], ['Sex', 'char', 0, 1], [
                  'BirthYear', 'integer', 0], ['FirstGames', 'varchar', 0, 20]])
  coach = table('coach', 2, [['OlympicID', 'varchar', 1, 10], [
                'Orientation', 'varchar', 0, 20]])
  country = table('country', 4, [['CName', 'varchar', 1, 30], ['AllTimeGold', 'integer', 0], [
                  'AllTimeSilver', 'integer', 0], ['AllTimeBronze', 'integer', 0]])
  event_schedule = table('event_schedule', 3, [['EventID', 'varchar', 1, 15], [
                          'EventDate', 'varchar', 1, 15], ['Location', 'varchar', 1, 30]])
  individual_results = table('individual_results', 3, [['EventID', 'varchar', 1, 15], [
                              'Olympian', 'varchar', 1, 25], ['Medal', 'varchar', 1, 10]],)
  participant = table('participant', 4, [['OlympicID', 'varchar', 1, 10], [
                      'LName', 'varchar', 1, 25], ['Fname', 'varchar', 1, 25], ['Country', 'varchar', 1, 30]])
  team = table('team', 7, [['TeamID', 'varchar', 1, 25], ['Member1', 'varchar', 1, 10], ['Member2', 'varchar', 1, 10], [
                'Member3', 'varchar', 1, 10], ['Member4', 'varchar', 0, 10], ['Member5', 'varchar', 0, 10], ['Member6', 'varchar', 0, 10]])
  team_results = table('team_results', 3, [['EventID', 'varchar', 1, 15], [
                        'Team', 'varchar', 1, 25], ['Medal', 'varchar', 1, 10]])
  global table_list
  table_list = [athlete, coach, country, event_schedule,
                individual_results, participant, team, team_results]
  return
    # parameters of table() are (table name, number of columns, column list)
    # column list is a nested list for each column in the table. Is of form [[column_name1, variable type, is not null specified, length of character field]]
    # For column_list[2], convention used is 0 if 'not null' is not specified in the constraints, 1 if 'not null' is specified in the constraints

if __name__ == '__main__':
  cur = cnx.cursor(buffered=True)
  print("\nENSF 300 ASSIGNMENT 5")
  print("\nCreated by: \n-Ethan Bensler\n-Liam Brennan\n-Andrew Duong\n-Joseph Duong")
  build_table_class()
  choicemenu()
  print("Thank you for using our program.")

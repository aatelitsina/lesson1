people = {
    'маша':{'city':'moscow', 'temperature':'23', 'wind':'west'},
    'петя':{'city':'samara', 'temperature':'30', 'wind':'east'},
    'олег':{'city':'piter', 'temperature':'00','wind':''}
}
name = input('Введите имя: ')
print(people.get(name,'такого имя нет'))
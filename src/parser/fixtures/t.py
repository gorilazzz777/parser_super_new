f = open('guide.json', 'r')
with open('g.json', 'w', encoding='utf8') as f1:
    f1.write(f.read())
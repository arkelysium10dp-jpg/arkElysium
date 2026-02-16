l = input("d:")
store = ""
docum = ""
for i in l:
    if i in r"\n":
        store += i
    if store == r"\n\n":
        input("DDDD")
        print(docum)
        docum = docum[:-3]
        print(docum)
print()
print()
print()
print(docum)
import wolframalpha

client = wolframalpha.Client('HE5YX8-WQJ3EE6W28')

while True:
    query = str(input('Query: '))
    res = client.query(query)
    output = next(res.results).text
    print(output)
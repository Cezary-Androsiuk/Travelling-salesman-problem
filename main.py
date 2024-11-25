
# data 1
nodes = [
    {'id': 1, 'name': 'city 1'}, 
    {'id': 2, 'name': 'city 2'}, 
    {'id': 3, 'name': 'city 3'}, 
    {'id': 4, 'name': 'city 4'}
]
connections = [
    {
        'node 1': 1,
        'node 2': 2,
        'weight': 0.2
    },
    {
        'node 1': 2,
        'node 2': 3,
        'weight': 0.4
    },
    {
        'node 1': 3,
        'node 2': 4,
        'weight': 0.8
    }
]

# data 2
nodes = [
    {
        'id': 1,
        'name': 'city 1',
        'connections': [
            {'node': 2, 'weight': 0.2}
        ]
    }, 
    {
        'id': 2,
        'name': 'city 2',
        'connections': [
            {'node': 3, 'weight': 0.4},
            {'node': 1, 'weight': 0.2}
        ]
    }, 
    {
        'id': 3,
        'name': 'city 3',
        'connections': [
            {'node': 4, 'weight': 0.8},
            {'node': 2, 'weight': 0.4}
        ]
    }, 
    {
        'id': 4,
        'name': 'city 4',
        'connections': [
            {'node': 3, 'weight': 0.8}
        ]
    }
]

if __name__ == '__main__':
    print('HelloWorld("print")')

    
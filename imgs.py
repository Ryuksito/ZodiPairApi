import os
paths = [
    '86b3fb32981740efbceb15e44036e988',
    '5479ed10e41742d5a82e9e919a5125e0',
    '9101d5c205974d7a9285237c9bd14ceb',
    '18139f8d2b0b4e86a69d2a20919c6d91',
    '286937237eb64e1b9594910ca07c33e2',
    'c3b2b5dde4b1481c8a98e2433936fc9e',
    'c4d1a44616744074b079999966775527',
    'd72e584223d24924af75b7294f3953e0',
    'edca788023af4dbb8e270e2c4caf523d',
    'fbc9cb8fd12d4a7a8abb3e9e86d14d3d'
]

for ur in paths:
    os.system("cls")
    path = f'app/images/users/{ur}/'
    url = '/'.join(path.split('/')[-2:-1]) + '/'
    print('\n'.join(['"'+url+img+'",' for img in os.listdir(path)]))  
    input("")
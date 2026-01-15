import json

""""
hal yang harus ada di tool definition:
1. nama function -> misalkan: calculator
2. description -> panggil functon ini ketika kamu ingin melakukan operasi matematika
3. parameter -> parameter apa yang perlu diisi pada function 

"""

basic_template ={
    'type':'function', 'function':{
        'name':'function_name',
        'decription':'penjelasan function apa ini',
        'parameters':{
            'type':'object', #type data param boleh berbeda-beda
            'properties':{
                'parameter1':{
                    'type':'String',
                    'description':'penjelasan type apa ini'
                },
                'parameter2':{
                    'type':'Float',
                    'description':'penjelasan type apa ini'
                }
            },
            'required':['parameter1'] # berarti parameter1 yang wajib di isi untuk memanggil functionnya
        }
    }
}

'''
5 parameter utama:
1.string
2.number
3.boolean
4.array
5.object
'''
# best practicenya adalah object

basic_template ={
    'type':'function', 'function':{
        'name':'function_name',
        'decription':'penjelasan function apa ini',
        'parameters':{
            'type':'object', #type data param boleh berbeda-beda
            'properties':{
                'parameter1':{
                    'type':'String',
                    'description':'penjelasan type apa ini'
                },
                'parameter2':{
                    'type':'Number',
                    'description':'penjelasan type apa ini'
                },
                'parameter3':{
                    'type':'Boolean',
                    'description':'penjelasan type apa ini'
                },
                'parameter4':{
                    'type':'Array',
                    'items':{'type':'String'},
                    'description':'penjelasan type apa ini'
                },
                'parameter5':{
                    'type':'Object',
                    'properties':{
                        'city':{'type':'String'},
                        'code':{'type':'Number'}    
                    },
                    'description':'penjelasan type apa ini'
                }
            },
            'required':['parameter1'] # berarti parameter1 yang wajib di isi untuk memanggil functionnya
        }
    }
}
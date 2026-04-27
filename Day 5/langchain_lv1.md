analisis program : 

line 4 -> sintaks ini untuk memanggil api key chatgpt dari framework langchain, dan langchain bisa memanggil model selain chatgpt, seperti google palm, anthropic, dll
line 5 -> sintaks ini untuk memanggil template prompt dari framework langchain, dan langchain bisa memanggil template prompt lain, seperti fewshot, zero shot, dll


Penjelasan :

arsitektur program ini menggunakan metode chain, dengan format:

prompt -> llm(openai) -> output

cara kerja sistem prompt di langchain sedikit dari biasanya yaitu:

prompt : 
sys
usr
ai

nah yang prompt system tidak akan ter-append saat user menginputkan sesuatu, jadi yang akan ter-append hanya prompt user dan ai saja, seperti ini:
prompt : 
sys
usr
ai
usr
ai
usr
ai
usr
ai
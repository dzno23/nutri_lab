from asyncio import constants
import re
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Dadospaciente, Pacientes



@login_required(login_url='/auth/logar')
def pacientes(request):

    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'pacientes.html', {'pacientes': pacientes})

    elif request.method == "POST":
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        if (len(nome.strip()) == 0) or (len(genero.strip()) == 0) or (len(idade.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos.')
            return redirect('/pacientes/')

        if not idade.isnumeric():
            messages.add_message(request, constants.ERROR, 'Digite uma idade válida.')
            return redirect('/pacientes/')
        
        paciente = Pacientes.objects.filter(email=email)

        if paciente.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse e-mail.')
            return redirect('/pacientes/')

        try:    
            paciente1 = Pacientes(nome=nome, genero=genero, idade=idade, email=email, telefone=telefone, nutri=request.user)
            paciente1.save()

            messages.add_message(request, constants.SUCCESS, 'Cadastro de paciente efetuado com sucesso.')
            return redirect('/pacientes/')

        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema, tente novamente.')
            return redirect('/pacientes')
        
    return render(request, 'pacientes.html')



@login_required(login_url='/auth/logar')
def dados_paciente_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'dados_paciente_listar.html', {'pacientes': pacientes})



@login_required(login_url='/auth/logar')
def dados_paciente(request, id):
    pacientes = get_object_or_404(Pacientes, id=id)
    if pacientes.nutri != request.user:
        messages.add_message(request, constants.ERROR, 'Este paciente não é seu.')
        return redirect('/dados_paciente/')
    
    if request.method == "GET":
        return render(request, 'dados_paciente.html', {'pacientes': pacientes})
    
    elif request.method == "POST":
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')

        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        trigliceridios = request.POST.get('triglicerídeos')
    
    try:
        dados = Dadospaciente(peso=peso, altura=altura, percentual_gordura=gordura, percentual_musculo=musculo)

        return redirect('/dados_paciente/')

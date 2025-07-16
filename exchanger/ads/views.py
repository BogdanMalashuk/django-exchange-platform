from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages


def ad_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    ads = Ad.objects.all().order_by('-created_at')

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads = ads.filter(category=category)
    if condition:
        ads = ads.filter(condition=condition)

    paginator = Paginator(ads, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {
        'ads': page_obj,
        'page_obj': page_obj,
        'categories': Ad.CATEGORY_CHOICES,
        'conditions': Ad.CONDITION_CHOICES,
        'query': query,
        'selected_category': category,
        'selected_condition': condition,
    })


@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            messages.success(request, f'Объявление "{ad.title}" успешно создано!')
            return redirect('ad_list')
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def ad_edit(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете редактировать это объявление.")
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, f'Объявление "{ad.title}" успешно изменено!')
            return redirect('ad_list')
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/ad_form.html', {
        'form': form,
        'form_title': 'Редактировать объявление'
    })


def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})


@login_required
def ad_delete(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)

    if request.user != ad.user:
        return redirect('ad_detail', ad_id=ad.id)

    if request.method == 'POST':
        ad.delete()
        messages.success(request, f'Объявление "{ad.title}" успешно удалено!')
        return redirect('ad_list')

    return redirect('ad_detail', ad_id=ad.id)


@login_required
def propose_exchange(request, ad_id):
    ad_receiver = get_object_or_404(Ad, id=ad_id)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_receiver = ad_receiver
            proposal.status = 'pending'
            proposal.save()
            return redirect('outgoing')
    else:
        form = ExchangeProposalForm(user=request.user)

    return render(request, 'proposals/proposal.html', {
        'form': form,
        'ad_receiver': ad_receiver
    })


@login_required
def incoming_proposals(request):
    user = request.user
    proposals = ExchangeProposal.objects.filter(ad_receiver__user=user).order_by('-created_at')
    status = request.GET.get('status')
    sender = request.GET.get('sender')

    if status:
        proposals = proposals.filter(status=status)

    if sender:
        proposals = proposals.filter(ad_sender__user__username__icontains=sender)

    return render(request, 'proposals/incoming.html', {
        'proposals': proposals,
        'filter_status': status,
        'filter_sender': sender,
    })


@login_required
def outgoing_proposals(request):
    user = request.user
    proposals = ExchangeProposal.objects.filter(ad_sender__user=user).order_by('-created_at')
    status = request.GET.get('status')
    receiver = request.GET.get('receiver')

    if status:
        proposals = proposals.filter(status=status)
    if receiver:
        proposals = proposals.filter(ad_receiver__user__username__icontains=receiver)

    return render(request, 'proposals/outgoing.html', {
        'proposals': proposals,
        'filter_status': status,
        'filter_receiver': receiver,
    })


@login_required
def accept_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)
    if request.user == proposal.ad_receiver.user and proposal.status == 'pending':
        proposal.status = 'accepted'
        proposal.save()
    return redirect('incoming')


@login_required
def reject_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)
    if request.user == proposal.ad_receiver.user and proposal.status == 'pending':
        proposal.status = 'rejected'
        proposal.save()
    return redirect('incoming')

from django.shortcuts import render
# django.views.genericからTemplateViewをインポート
from django.views.generic import TemplateView, ListView

from django.views.generic import CreateView

from django.urls import reverse_lazy

from .forms import PhotoPostForm

from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required

from .models import PhotoPost

from django.views.generic import DetailView

from django.views.generic import DeleteView

class IndexView(ListView): 
    '''トップページのビュー
    '''
    # index.htmlをレンダリングする
    template_name ='index.html'
    
    queryset = PhotoPost.objects.order_by('-posted_at')
    
    paginate_by = 9
    
@method_decorator(login_required, name = 'dispatch')
class CreatePhotoView(CreateView):
    form_class = PhotoPostForm
    
    template_name = "post_photo.html"

    success_url = reverse_lazy('photo:post_done')
    
    def form_valid(self, form):
        postdata = form.save(commit = False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)

class PostSuccessView(TemplateView):
    template_name = 'post_success.html'
    

class CategoryView(ListView):
    '''カテゴリページのビュー

    Attributes:
      template_name:レンダリングするテンプレート
      paginate_by:1ページに表示するレコードの件数
    '''
    # index.htmlをレンダリングする
    template_name = 'index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
        '''クエリを実行する

        self.kwargsの取得が必要なため、クラス変数querysetではなく
        get_queryset()のオーバーライドによりクエリを実行する

        Returns:
          クエリによって取得されたレコード
        '''
        # self.kwargsでキーワードの辞書を取得し、
        # categoryキーの値(Categorysテーブルのid)を取得
        category_id = self.kwargs['category']
        # filter(フィールド名=id)で絞り込む
        categories = PhotoPost.objects.filter(category=category_id).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return categories

class UserView(ListView):
    template_name = 'index.html'
    paginate_by = 9
    
    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = PhotoPost.objects.filter(
            user= user_id).order_by('-posted_at')
        return user_list
    
    
class DetailView(DetailView):
    template_name='detail.html'
    model = PhotoPost
    
class MypageView(ListView):
    template_name='mypage.html'
    paginate_by = 9
    def get_queryset(self):
        queryset = PhotoPost.objects.filter(
            user = self.request.user).order_by('-posted_at')
        
        return queryset
    
    
class PhotoDeleteView(DeleteView):
    model = PhotoPost
    template_name = 'photo_delete.html'
    success_url = reverse_lazy('photo:mypage')
    def delete(self, request, *args,**kwargs):
        
        return super().delete(request, *args, **kwargs)
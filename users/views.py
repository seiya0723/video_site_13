from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse

from .models import CustomUser,FollowUser,BlockUser
from .serializer import FollowUserSerializer,BlockUserSerializer,IconSerializer

from rest_framework import views


#ユーザーページの表示
class UserSingleView(views.APIView):

    def get(self, request, pk, *args, **kwargs):

        user    = CustomUser.objects.filter(id=pk).first()


        #このユーザーがフォローしているユーザー、ブロックしているユーザーの一覧
        follow_users = FollowUser.objects.filter(from_user=pk)
        block_users  = BlockUser.objects.filter(from_user=pk)

        #このユーザーをフォローしているユーザー、ブロックしているユーザーの一覧
        follower_users    = FollowUser.objects.filter(to_user=pk)
        blocker_users     = BlockUser.objects.filter(to_user=pk)

        context = { "user":user,
                    "follow_users":follow_users,
                    "block_users":block_users,
                    "follower_users":follower_users,
                    "blocker_users":blocker_users,
                }

        return render(request, "tube/user.html", context)

single  = UserSingleView.as_view()






class UserFollowView(LoginRequiredMixin,views.APIView):

    def get(self,request, pk,*args, **kwargs):


        followers   = FollowUser.objects.all()
        context     = {"followers":followers,
                       }

        return render(request, 'tube/follow.html', context)


    def post(self,request,pk,*args,**kwargs):

        followusers  = FollowUser.objects.filter(from_user=request.user.id,to_user=pk) #from_userは自分自身。to_user はフォローした相手。

        json    = { "error":False }

        #すでにある場合は該当レコードを削除、無い場合は挿入
        #TIPS:↑メソッドやビュークラスを切り分けてしまうと、多重に中間テーブルへレコードが挿入されてしまう可能性があるため1つのメソッド内で分岐するやり方が無難。
        if followusers:
            print("ある。フォロー解除。")
            followusers.delete()

            return JsonResponse(json)
        else:
            print("無い")

        data        = { "from_user":request.user.id,"to_user":pk }
        serializer  = FollowUserSerializer(data=data)

        if serializer.is_valid():
            print("フォローOK")
            serializer.save()
        else:
            print("フォロー失敗")
            json["error"]   = True

        return JsonResponse(json)


follow   = UserFollowView.as_view()


class UserBlockView(LoginRequiredMixin,views.APIView):

    def post(self,request,pk,*args,**kwargs):

        blockusers  = BlockUser.objects.filter(from_user=request.user.id,to_user=pk)

        json    = { "error":False }

        if blockusers:
            print("ある。ブロック解除。")
            blockusers.delete()

            return JsonResponse(json)
        else:
            print("無い")

        data        = { "from_user":request.user.id,"to_user":pk }
        serializer  = BlockUserSerializer(data=data)

        if serializer.is_valid():
            print("ブロックOK")
            serializer.save()
        else:
            print("ブロック失敗")
            json["error"]   = True

        return JsonResponse(json)


block   = UserBlockView.as_view()



class UserEditView(LoginRequiredMixin,views.APIView):

    def post(self,request, *args,**kwargs):

        print(request.data)
        print(request.user.id)
        instance = CustomUser.objects.get(id=request.user.id)

        serializer = IconSerializer(instance, data=request.data)

        if serializer.is_valid():
            print("validation OK")
            serializer.save()
            json = {"error": False,
                    "message":"アイコンが登録されました。"}

        else:
            print("バリデーションエラー")
            json = {"error": True,
                    "message": "アイコン登録に失敗しました。"}


        return JsonResponse(json)

useredit   = UserEditView.as_view()


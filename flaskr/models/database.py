from flaskr import db
from datetime import datetime
from flask_login import UserMixin

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    ingredient_name = db.Column(db.String(255))  # 材料名
    quantity = db.Column(db.String(255))  # 分量
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時

class Step(db.Model):
    __tablename__ = 'step'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    step_number = db.Column(db.Integer) #手順番号
    content = db.Column(db.String(255))  # 手順の説明文
    step_photo_path = db.Column(db.String(255))  # 手順の説明画像
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時

class Recipe_ingredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)  # レシピtableへの関連付け番号
    ingredient_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True) # 材料tableへの関連付け番号
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時

class Recipe_step(db.Model):
    __tablename__ = 'recipe_step'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)  # レシピtableへの関連付け番号
    step_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True) # 手順tableへの関連付け番号
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号(主キー)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) # (外部キー)
    title = db.Column(db.String(255))  # 料理名
    step_photo_path = db.Column(db.String(255))  # 料理の完成画像
    memo = db.Column(db.String(255))  # メモ
    cook_time = db.Column(db.Integer)  # 作成時間(分)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    username = db.Column(db.String(255), nullable=False)  # ユーザー名
    email = db.Column(db.String(255), nullable=False, unique=True)  # メールアドレス
    password = db.Column(db.String(255), nullable=False)  # パスワード
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時

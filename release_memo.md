# リリース時に行うことメモ

1. __init__.pyのバージョンを修正  
`__version__ = "x.y.z"`  
バージョニングルール  
x:メジャーバージョン（後方互換のない破壊的な機能追加）  
y:マイナーバージョン（後方互換の機能追加）  
z:パッチバージョン（後方互換のバグ修正）
2. README.mdを最新化
3. example.ipynを追加機能に合わせ修正
4. タグ付け
5. pypiテスト環境リリース後の動作確認（example.ipyn）
6. リリースノート作成
7. pypi本番環境リリース後の動作確認（example.ipyn）
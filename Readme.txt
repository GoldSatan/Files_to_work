****************************************************************************************************************************************************************************************
������� ����� �������� - dist
� ����� addition - ����������� ������� ����� � ���� ������� �� ��������� ���� for file � ����� ��������� �� 
�������� ������� ��������� CalculateCorpusData.
��� ������ ������ �������� ��������� ����� dist �� ��������� mergen_script.exe
� ����� .exe ���� � ��� ����������� 3 ����������(3 ����� ��� ��������� ������� ��� �� ������� TF-IDF):

1 ���������� - PreProcessingApp - ��������� �������� ���� ������ ��� ���������� ������������ ����� ���������
ϳ������� ����������:
Select stop list file - ����������� ��������� ���� � ���� ������� ���� ������������ � ����� addition
Select source folder - ������� ����� � ����� ����� ������
Select target folder - ������� ���� �������� ������ �� ������� ������������
Select language - ������� ���� ������
Select stop word mode - ������� �� � ���� ������� �� ����������� � ����� ��� ������ : 
	Remove - ��������,
	Replace - �������, 
	Asls - �������� � �����.
Replace stop word as - ���� � ����� Select stop word mode ������ Replace �� � ����� ����� �� ������� �� ��� ����� ������� ���� �����
Select processing mode - ������� �� ������������� ����� � ����� ������� �� ������� ������ �����.
	Stemmer � ������ � ����� ����� ������
	Lemmatize � ������� ����� � ����� ������� �� ���������
	Asls � ������ ����� � ������� ������
Select sentenct terminator mode -ĳ� � ��������� ���� (.?!) 
	Remove � ������� �� �������,
	Replace � ����� �� �� ������� �� ������� � ����� Replace sentence terminators(.!?) as:
Select cipher(0-9) mode - ĳ� � ������� : Asls - ������ ��, Remove �������

2 ���������� - CalculateCorpusData - ������ � ����� ������ ��� ������� ����� ������������ �� ������� � ��� ������ ������� ��� ��� � ����� ����
� ������ ������������ ��������.�� ���� �������� �� ������ ����� � �������� ����� ������ � �� ����� ��������
2 ����� �������� � ����� \dist\Result_of_Corpus_Data ���������� .csv  _info �� _dict, � _info �������� ������� ���������� �� ��� ������
� � _dict �������� ������� ��� � ������ ������������ ��������:
	������� A - �����
	������� B - Sum F (��������� �������)
	������� � � f (������� �������)
	������� D - fw (������� �������)
	������� E - nt (�-��� ���������, �� ��������� �����)
	������� F - sigma ( ���.��.���������)
	������� G - sigmaw (���. ��. ���. �� ����� fw)
	������� H - Sum (F^2 / L)
	������� I - Sum (F^2 / L^2)

3 ���������� - CalculateKeynessRelative_AddDictTextToIndex � �� �� ���� �� ����������� �������� � 2 ���������� ����� _info �� _dict �� ������ �������� ����� � ���� ����
� �� ����� � ����� \dist\Result_of_Keyness_Relative �������� ������� ������ ��� ������ �������� ������� TF-IDF
	������� A � ���� �����
	������� B - �����
	������� � � ������ �����
	������� D � ��������� ������ �����
	������� E � ��������� �������
	������� F � ³������ �������

**********************************************************************************************************************************************************





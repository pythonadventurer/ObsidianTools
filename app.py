from lib import *

vault_folder = r"D:/Rob/InfoCenter"
moc_folder_rel = r"Church_Journal"
# document_folder = r"D:\Rob\The_Compendium\Documents"
# document_folder = r"C:\Users\robf.PCS\Downloads\The_Compendium\Documents"
document_folder = r"D:\Rob\Downloads\Compendium\Documents"


my_assistant = FilingAssistant(document_folder)
my_assistant.process_files()















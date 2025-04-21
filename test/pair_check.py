from Bio import SeqIO
fasta_file = "./download/OLD.fasta"
fasta_file = "./download/2023-01-01_2023-12-31.fasta"

tgt_sequences = {}
src_sequences = {}
for record in SeqIO.parse(fasta_file, "fasta"):
    tgt_sequences[record.id.split("|")[-1]] = record.seq
for record in SeqIO.parse(fasta_file, "fasta"):
    src_sequences[record.id.split("|")[-1]] = record.seq

missing_key = []
unpair_key = []
for k in tgt_sequences:
    if k not in src_sequences:
        missing_key.append(k)
        continue
    if tgt_sequences[k] != src_sequences[k]:
        unpair_key.append(k)
print(missing_key)
print(f"{len(missing_key)}/{len(tgt_sequences)}")
print(f"{len(unpair_key)}/{len(tgt_sequences)}")
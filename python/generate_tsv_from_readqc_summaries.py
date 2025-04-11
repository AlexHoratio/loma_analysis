import re
import os 

def main():
	generate_tsv_from_readqc_summaries(['SRR29980928', 'SRR29980939', 'SRR29980950', 'SRR29980957', 'SRR29980958', 'SRR29980959', 'SRR29980960', 'SRR29980961', 'SRR29980962', 'SRR29980963', 'SRR29980964', 'SRR29980965', 'SRR29980966', 'SRR29980967', 'SRR29980968', 'SRR29980969', 'SRR29980970', 'SRR29980971', 'SRR29980973', 'SRR29980974', 'SRR29980975', 'SRR29980976', 'SRR29980977', 'SRR29980978', 'SRR29980979', 'SRR29980980', 'SRR29980981', 'SRR29980982', 'SRR29980983', 'SRR29980984', 'SRR29980985', 'SRR29980986', 'SRR29980987', 'SRR29980988', 'SRR29980989', 'SRR29980990', 'SRR29980991', 'SRR29980992', 'SRR29980993', 'SRR29980994', 'SRR29980995', 'SRR29980997', 'SRR29980998', 'SRR29980999', 'SRR29981000', 'SRR29981001', 'SRR29981002', 'SRR29981003', 'SRR29981004', 'SRR29981005', 'SRR29981006', 'SRR29981007', 'SRR29981015', 'SRR29981026', 'SRR29981037', 'SRR29981050', 'SRR29981061', 'SRR29981072', 'SRR29981083', 'SRR29981084', 'SRR29981085'])

def generate_tsv_from_readqc_summaries(run_accessions, run_directory=""):
	#print(run_accessions)

	readqc_summary_data = {
#		"SRR29980928" : {
#			"pre" : {
#				"number_of_reads" : 9999,
#				"mean_read_length" : 9999,
#				"read_n50" : 9999,
#				"mean_read_quality" : 9999,
#				"total_bases_mbp" : 9999,
#			}
#		}
		 
	}

	for run_acc in run_accessions:
		summary_file = open((run_directory) + run_acc + "/summary/" + run_acc + ".RUN01.readqc_report.html")
		summary_file_lines = summary_file.readlines()

		run_acc_data = {}

		for i in range(len(summary_file_lines)):
			if "Number of reads" in summary_file_lines[i]:
				run_acc_data["number_of_reads"] = summary_file_lines[i + 1].strip().replace("<td>", "").replace("</td>", "")
			if "Mean read length" in summary_file_lines[i]:
				run_acc_data["mean_read_length"] = summary_file_lines[i + 1].strip().replace("<td>", "").replace("</td>", "")
			if "<b>Read N" in summary_file_lines[i]:
				run_acc_data["read_n50"] = summary_file_lines[i + 1].strip().replace("<td>", "").replace("</td>", "")
			if "Mean read quality" in summary_file_lines[i]:
				run_acc_data["mean_read_quality"] = summary_file_lines[i + 1].strip().replace("<td>", "").replace("</td>", "")
			if "Total bases" in summary_file_lines[i]:
				run_acc_data["total_bases_mbp"] = summary_file_lines[i + 1].strip().replace("<td>", "").replace("</td>", "")

		contig_coverage_loc = (run_directory) + run_acc + "/assembly/contig_qc/coverage/" + run_acc + ".coverage.txt"

		if os.path.exists(contig_coverage_loc):
			contig_coverage_file = open(contig_coverage_loc)
			contig_coverage_lines = contig_coverage_file.readlines()
			run_acc_data["contig_count"] = str(len(contig_coverage_lines) - 1)

		else:
			run_acc_data["contig_count"] = "0"


		assembly_stats_loc = (run_directory) + run_acc + "/assembly/bin_QC/assembly_stats/" + run_acc + ".RUN01.assembly_stats.csv"

		if os.path.exists(assembly_stats_loc):
			assembly_stats_file = open(assembly_stats_loc)
			assembly_stats_lines = assembly_stats_file.readlines()
			run_acc_data["bin_count"] = str(len(assembly_stats_lines) - 1)

		else:
			run_acc_data["bin_count"] = "0"

		readqc_summary_data[run_acc] = run_acc_data

	readqc_summary_tsv = "run_accession	"
	readqc_summary_colnames = ["number_of_reads", "mean_read_length", "read_n50", "mean_read_quality", "total_bases_mbp", "contig_count", "bin_count"]

	for i in range(len(readqc_summary_colnames)):
		readqc_summary_tsv += readqc_summary_colnames[i] + ("\t" if (i + 1) < len(readqc_summary_colnames) else "")

	for run_acc in readqc_summary_data.keys():
		readqc_summary_tsv += "\n" + run_acc + "\t"
		for i in range(len(readqc_summary_colnames)):
			readqc_summary_tsv += readqc_summary_data[run_acc][readqc_summary_colnames[i]] + ("\t" if (i + 1) < len(readqc_summary_colnames) else "")

	return readqc_summary_tsv


if __name__ == "__main__":
	main()
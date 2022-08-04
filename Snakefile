#configfile: "config.yaml"

rule segment_vcf:
	input:
		"cpp/config_sample"
	output:
		"data/segments/test_segment"
	shell:
		"bash ./bash/segmentVCF.sh"

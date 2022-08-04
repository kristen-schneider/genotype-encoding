configfile: "config.yaml"

rule all:
	input:
		expand(
		
		)

rule segment_vcf:
	input:
		""
	output:
		"vcf_segment"

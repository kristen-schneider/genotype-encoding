configfile: "config.yaml"

rule all:
	input:
		expand(config["segments_out_dir"], segments.encoding.done)

rule segment_vcf_COMPILE:
	input:
		main=expand({config[src_dir]}, "main.cpp"),
		read_config=expand(config[src_dir], "read_config.cpp"),
		map_encodings=expand(config[src_dir], "map_encodings.cpp"),
		slice_vcf=expand(config[src_dir], "slice_vcf.cpp"),
		encode_vcf=expand(config[src_dir], "encode_vcf.cpp"),
		include=config[include_dir]

	output:
		bin=expand(config[bin_dir], "segment")
	message:
		"Compiling--slice vcf into segments and encode"
	shell:
		"g++ {input.main}" \
			" {input.read_config}" \
			" {input.map_encodings}" \
			" {input.slice_vcf}" \
			" {input.encode_vcf}" \
			" -I {input.include}" \
			" -lhts" \
			" -o {output.bin}"
		

rule segment_vcf_RUN:
	input:
		bin=expand(config[bin_dir], "segment"),
		config_file=config[segments_config]
	output:
		done=expand(config[segments_out_dir], "segments.encoding.done")
	message: 
		"Executing--slice vcf into segments and encode"
	shell:
		"./{input.bin} {input.config_file}",
		"touch " expand(config[segments_out_dir], "segments.encoding.done")

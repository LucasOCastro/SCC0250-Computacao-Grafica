#version 450 core

#define MAX_LIGHTS 3
struct Light {
    vec3 position;
    vec3 color;
};

// Recebe do programa
// -- Camera e luzes
uniform vec3 viewPos; // posicao do observador/camera
uniform vec3 ambientLightColor;
uniform Light lights[MAX_LIGHTS]; // luzes
uniform int numLights;
uniform bool lit = true;
// -- Material atual
uniform sampler2D tex; // textura
uniform vec3 ka; // coeficiente de reflexao ambiente
uniform vec3 kd; // coeficiente de reflexao difusa
uniform vec3 ks; // coeficiente de reflexao especular
uniform float ns; // expoente de reflexao especular

// Recebe da vertex shader
in vec2 v_uv;
in vec3 v_fragPos; //posicao do fragmento (i.e., posicao na superficie onde a iluminacao sera calculada)
in vec3 v_normal;

// Output da fragment shader
out vec4 fragColor;

// TODO use light falloff

vec3 calc_diffuse(vec3 color, vec3 lightDir, vec3 norm) {
	float diff = max(dot(norm, lightDir), 0.0);
    return kd * diff * color;
}

vec3 calc_specular(vec3 color, vec3 viewDir, vec3 lightDir, vec3 norm) {
	vec3 specDir = normalize(reflect(-lightDir, norm)); // Phong usa reflection
	// vec3 specDir = normalize(viewDir + lightDir); // Blinn-Phong usa half vector ao invés de reflection
    float NdotH = dot(norm, specDir);
    if (NdotH <= 0.0) return vec3(0.0); // Usar if ao invés de max consertou um erro de renderização

    float spec = pow(NdotH, ns);
    return ks * spec * color;
}

void main(){
    vec4 texture = texture(tex, v_uv);
    if (texture.a < 0.9) // alpha threshold
        discard;

	// Não é ideal usar if ao invés de outro shader
	if (!lit) {
		fragColor = texture;
		return;
	}
    
	vec3 ambient = ka * ambientLightColor;

	// calculando reflexao difusa e especular
	vec3 viewDir = normalize(viewPos - v_fragPos);
	vec3 norm = normalize(v_normal);
	vec3 diffuse = vec3(0.0);
	vec3 specular = vec3(0.0);
	for (int i = 0; i < MAX_LIGHTS; i++) {
		if (i >= numLights) break;
		Light light = lights[i];
		vec3 lightDir = normalize(light.position - v_fragPos);

		diffuse += calc_diffuse(light.color, lightDir, norm);
		specular += calc_specular(light.color, viewDir, lightDir, norm);
	};
	
	// aplicando o modelo de iluminacao
	fragColor = vec4((ambient + diffuse + specular), 1.0) * texture;
}
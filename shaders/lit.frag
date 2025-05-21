#version 450 core

struct Light {
    vec3 position;
    vec3 color;
};

// Recebe do programa
// -- Camera e luzes
uniform vec3 viewPos; // posicao do observador/camera
uniform vec3 ambientLightColor;
uniform Light lights[3]; // luzes
uniform int numLights;
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

vec3 calc_diffuse(vec3 color, vec3 lightDir, vec3 norm) {
	float diff = max(dot(norm, lightDir), 0.0); // verifica limite angular (entre 0 e 90)
	vec3 diffuse = kd * diff * color; // iluminacao difusa
    return diffuse;
}

vec3 calc_specular(vec3 color, vec3 lightDir, vec3 norm) {
	vec3 viewDir = normalize(viewPos - v_fragPos); // direcao do observador/camera
	vec3 reflectDir = normalize(reflect(-lightDir, norm)); // direcao da reflexao
	float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
	vec3 specular = ks * spec * color;
	return specular;
}

void main(){
    vec4 texture = texture(tex, v_uv);
    if (texture.a < 0.9) // alpha threshold
        discard; 
    
	vec3 ambient = ka * ambientLightColor;

	// calculando reflexao difusa e especular
	vec3 norm = normalize(v_normal);
	vec3 diffuse = vec3(0.0);
	vec3 specular = vec3(0.0);
	for (int i = 0; i < numLights; i++) {
		Light light = lights[i];
		vec3 lightDir = normalize(light.position - v_fragPos);
		vec3 currDiffuse = calc_diffuse(light.color, lightDir, norm);
		vec3 currSpecular = calc_specular(light.color, lightDir, norm);

		diffuse += currDiffuse;
		specular += currSpecular;
	};
	
	// aplicando o modelo de iluminacao
	vec4 result = vec4((ambient + diffuse + specular), 1.0) * texture; // aplica iluminacao
	fragColor = result;
}
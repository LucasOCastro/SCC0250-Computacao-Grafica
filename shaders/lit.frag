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
uniform Light lights[MAX_LIGHTS];
uniform int numLights;
uniform bool lit; // Se false, retorna a cor da textura sem aplicar luz.
// -- Material atual
uniform sampler2D tex; // textura
uniform float colorMultiplier; // multiplica a cor da textura
uniform vec3 ka; // coeficiente de reflexao ambiente
uniform vec3 kd; // coeficiente de reflexao difusa
uniform vec3 ks; // coeficiente de reflexao especular
uniform float ns; // expoente de reflexao 
uniform bool lightBackfaces; // Se true, ilumina ambas as faces do modelo (útil para grama e modelos de 1 face)

// Recebe da vertex shader
in vec2 v_uv;
in vec3 v_fragPos;
in vec3 v_normal;

// Output da fragment shader
out vec4 fragColor;

vec3 calc_diffuse(vec3 color, vec3 lightDir, vec3 norm) {
	float diff = max(dot(norm, lightDir), 0.0);
    return kd * diff * color;
}

vec3 calc_specular(vec3 color, vec3 viewDir, vec3 lightDir, vec3 norm) {
	// Phong
    vec3 specDir = normalize(reflect(-lightDir, norm));
    float specAngle = max(dot(viewDir, specDir), 0.0);

	// Blinn-Phong
	// vec3 halfDir = normalize(viewDir + lightDir);
	// float specAngle = max(dot(norm, halfDir), 0.0);

	if (specAngle <= 0.0) return vec3(0.0); // Evita erro de renderização
    float spec = pow(specAngle, ns);
    return ks * spec * color;
}

float calc_attenuation(float d) {
	const float constant = 1.0;
	const float linear = 0.01;
	const float quadratic = 0.001;
    return 1.0 / (constant + linear * d + quadratic * d * d);
}

void main(){
    vec4 texColor = texture(tex, v_uv);
	texColor = vec4(texColor.rgb * colorMultiplier, texColor.a);
	if (texColor.a < 0.9) discard;

	// Não é ideal usar if ao invés de outro shader
	if (!lit) {
		fragColor = texColor;
		return;
	}

	// Normalmente backfaces são descartados, mas por especificação do trabalho apenas ignoramos iluminação.
	if (!gl_FrontFacing && !lightBackfaces) {
		fragColor = texColor;
		return;
	}
    
	// Calculando reflexao difusa e especular
	vec3 viewDir = normalize(viewPos - v_fragPos);
	vec3 norm = normalize(v_normal);
	vec3 diffuse = vec3(0.0);
	vec3 specular = vec3(0.0);
	for (int i = 0; i < MAX_LIGHTS; i++) {
		if (i >= numLights) break;

		// Precisamos da distância pra atenuação de qualquer forma, então nem usamos o normalize
		Light light = lights[i];
		vec3 vecToLight = light.position - v_fragPos;
		float distToLight = length(vecToLight);
		vec3 lightDir = vecToLight / distToLight;

		// Atenuação aplicada em cada valor
		float attenuation = calc_attenuation(distToLight);
		diffuse += calc_diffuse(light.color, lightDir, norm) * attenuation;
		specular += calc_specular(light.color, viewDir, lightDir, norm) * attenuation;
	};
	
	// Aplicando o modelo de iluminacao
	vec3 ambient = ka * ambientLightColor;
	fragColor = vec4(texColor.rgb * (ambient + diffuse + specular), 1.0);
}

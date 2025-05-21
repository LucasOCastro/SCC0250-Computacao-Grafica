#version 450 core

// Vem no vértice
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec2 in_uv;
layout(location = 2) in vec3 in_normal;

// Recebe do programa
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// Vai pra fragment shader
out vec2 v_uv;
out vec3 v_fragPos; //posicao do fragmento (i.e., posicao na superficie onde a iluminacao sera calculada)
out vec3 v_normal;

void main() {
    gl_Position = projection * view * model * vec4(in_position, 1.0);
	v_uv = in_uv;
	v_fragPos = vec3(model * vec4(in_position, 1.0));
	// v_normal = vec3(model * vec4(in_normal, 1.0));
	v_normal = normalize(mat3(transpose(inverse(model))) * in_normal);
}

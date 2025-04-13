#version 400

// Vem no vértice
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec2 in_uv;

// Recebe do programa
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// Vai pra fragment shader
out vec2 v_uv;

void main() {
    gl_Position = projection * view * model * vec4(in_position,1.0);
    v_uv = in_uv;
}

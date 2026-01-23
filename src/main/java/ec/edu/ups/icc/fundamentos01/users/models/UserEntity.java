package ec.edu.ups.icc.fundamentos01.users.models;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import ec.edu.ups.icc.fundamentos01.core.entities.BaseModel;
import ec.edu.ups.icc.fundamentos01.products.models.ProductEntity;
import ec.edu.ups.icc.fundamentos01.security.models.RoleEntity;
import ec.edu.ups.icc.fundamentos01.security.models.RoleName;
import jakarta.persistence.*;

/**
 * ENTIDAD: User (Usuario del sistema)
 * 
 * Representa un usuario con sus credenciales y roles.
 * Relaciones:
 * - ManyToMany con RoleEntity (un usuario puede tener varios roles)
 * - OneToMany con ProductEntity (un usuario puede tener varios productos)
 */
@Entity
@Table(name = "users")
public class UserEntity extends BaseModel {

    @Column(nullable = false, length = 150)
    private String name;

    @Column(nullable = false, unique = true, length = 150)
    private String email;

    /**
     * Contraseña HASHEADA con BCrypt
     * 
     * NUNCA se almacena en texto plano.
     * Ejemplo hash: $2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
     * 
     * Al registrar usuario:
     * String plainPassword = "Secure123";
     * String hashedPassword = passwordEncoder.encode(plainPassword);
     * user.setPassword(hashedPassword); // ← Esto se guarda en BD
     * 
     * Al hacer login:
     * passwordEncoder.matches("Secure123", user.getPassword()); // true/false
     */
    @Column(nullable = false)
    private String password;

    // ============== NUEVA RELACIÓN CON ROLES ==============

    /**
     * Relación ManyToMany con Roles
     * 
     * @ManyToMany: Un usuario puede tener múltiples roles
     *              Un rol puede estar asignado a múltiples usuarios
     * 
     *              fetch = FetchType.EAGER:
     *              - Carga los roles AUTOMÁTICAMENTE al consultar el usuario
     *              - Necesario porque Spring Security necesita los roles al
     *              autenticar
     *              - Sin EAGER, tendríamos LazyInitializationException al acceder a
     *              roles
     * 
     * @JoinTable: Crea tabla intermedia user_roles
     *             name = "user_roles": Nombre de la tabla intermedia en BD
     *             joinColumns: Columna que referencia a esta entidad (users.id)
     *             inverseJoinColumns: Columna que referencia a RoleEntity
     *             (roles.id)
     * 
     *             Tabla user_roles en BD:
     *             CREATE TABLE user_roles (
     *             user_id BIGINT REFERENCES users(id),
     *             role_id BIGINT REFERENCES roles(id),
     *             PRIMARY KEY (user_id, role_id)
     *             );
     * 
     *             Set<RoleEntity>:
     *             - Set (no List) evita duplicados
     *             - HashSet inicializado para evitar NullPointerException
     * 
     *             Ejemplo de uso:
     *             UserEntity user = userRepository.findById(1L);
     *             user.getRoles(); // ← Ya cargados por EAGER
     *             [RoleEntity(ROLE_USER), RoleEntity(ROLE_ADMIN)]
     */
    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable(name = "user_roles", joinColumns = @JoinColumn(name = "user_id"), inverseJoinColumns = @JoinColumn(name = "role_id"))
    private Set<RoleEntity> roles = new HashSet<>();

    // ============== RELACIÓN EXISTENTE CON PRODUCTOS ==============
    /**
     * Relación One-to-Many con Product
     * Un usuario puede tener múltiples productos
     */
    @OneToMany(mappedBy = "owner", fetch = FetchType.LAZY, cascade = CascadeType.ALL, orphanRemoval = true)
    private List<ProductEntity> products = new ArrayList<>();

    // ============== CONSTRUCTORES ==============
    public UserEntity() {
    }

    public UserEntity(String name, String email, String password) {
        this.name = name;
        this.email = email;
        this.password = password;
    }

    // ============== GETTERS Y SETTERS ==============
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
    
    public Set<RoleEntity> getRoles() {
        return roles;
    }

    public void setRoles(Set<RoleEntity> roles) {
        this.roles = roles;
    }

    public List<ProductEntity> getProducts() {
        return products;
    }

    public void setProducts(List<ProductEntity> products) {
        this.products = products;
    }

    // ============== MÉTODOS HELPER ==============

    /**
     * Agrega un rol al usuario
     */
    public void addRole(RoleEntity role) {
        this.roles.add(role);
        role.getUsers().add(this);
    }

    /**
     * Verifica si el usuario tiene un rol específico
     */
    public boolean hasRole(RoleName roleName) {
        return this.roles.stream()
                .anyMatch(role -> role.getName().equals(roleName));
    }


}